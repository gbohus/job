import logging
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from oci.generative_ai_inference import GenerativeAiInferenceClient
from oci.generative_ai_inference.models import ChatDetails, CohereChatRequest, OnDemandServingMode
from constants import VALID_CATEGORIES, VERTICAL_SUMMARIES
from utils import setup_oci_client, error_handler
from text_processing import extract_key_content
import re
import functools
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
from config import OCI_COMPARTMENT_ID, OCI_MODEL_ID, MAX_TOKENS, TEMPERATURE, FREQUENCY_PENALTY, TOP_P, TOP_K
import json

logger = logging.getLogger(__name__)

# Download NLTK data (if not already downloaded)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)


def construct_prompt(key_content, customer, relevant_data):
    # Convert categories to string
    categories = ', '.join(VALID_CATEGORIES)
    
    # Prepare company info
    company_info = f"""
1. Customer: {relevant_data['Customer']}
2. City: {relevant_data['Maximum of City']}
3. Country: {relevant_data['Maximum of Country']}
4. State/Province: {relevant_data['Maximum of State/Province']}
5. Web Address: {relevant_data['Web Address']}
6. Homepage summary: {key_content['home']['summary']}
7. Homepage top keywords: {', '.join(key_content['home']['top_keywords'])}
8. About page summary: {key_content['about']['summary']}
9. About page top keywords: {', '.join(key_content['about']['top_keywords'])}
10. Combined top keywords: {', '.join(key_content['combined_keywords'])}
11. Product page exists: {'Yes' if key_content['product_exists'] else 'No'}"""

    # Construct the full prompt
    full_prompt = f"""
Customer: {customer}

## Company Information
{company_info}

## Acceptable Business Industries
{categories}

## Vertical Summaries
{format_vertical_summaries(VERTICAL_SUMMARIES)}

## Keyword Usage and Confidence Assessment:

Each vertical summary includes a set of keywords categorized into tiers:

1. Tier 1 (Primary Keywords): These are the main keywords most strongly associated with the vertical.
2. Tier 2 (Secondary Keywords): These keywords are still relevant but less specific to the vertical.
3. Tier 3 (Tertiary Keywords): These keywords are broadly related to the vertical but may also apply to other industries.
4. Negative Keywords: The presence of these keywords may indicate that the business is not primarily in this vertical.

Use these keywords to guide your classification, but remember to consider the overall context of the business description, not just the presence or absence of specific keywords.

Assess your classification confidence based on the keywords present and overall business analysis:

- High confidence: Strong alignment with vertical description, supported by multiple Tier 1 keywords and overall business context
- Medium confidence: Moderate alignment with vertical description, mainly supported by Tier 2 keywords and some aspects of the business context
- Low confidence: Weak alignment with vertical description, only supported by Tier 3 keywords or limited aspects of the business context
- Requires review: Presence of negative keywords, conflicting information, or highly ambiguous business description

If negative keywords are found or there's conflicting information, prioritize your analysis of the overall business context over keyword matches.

## General Instructions:
1. Analyze the provided company information and categorize the business into one of the Acceptable Business Industries listed above. 
2. Choose ONE primary category and ONE secondary category. 
3. Do not use any categories not in this list.
4. If a current category is provided, evaluate whether you agree or disagree with this categorization based on your analysis.

## Critical Instructions:

1. Think through step by step as you analyze the company information and vertical summaries.
2. Thoroughly read and understand the company information and vertical summaries.
3. Consider the overall context, business activities, and industry focus described in the company information.
4. Compare the company's activities and focus to the provided vertical summaries.
5. Make your categorization based on the best overall match between the company information and the vertical summaries.
6. While keywords can be indicative, prioritize understanding the company's core business over simple keyword matching.
7. If the company clearly states it's a non-profit organization or mentions "501(c)3", strongly consider the 'Social Impact' category if it's available.
8. If a current category is provided, critically evaluate whether it accurately represents the company based on your analysis.
9. For companies with multiple distinct business lines, focus on identifying and categorizing the most dominant or core business activity.
10. In cases of conflicting information, rely more heavily on your analysis of the overall business context rather than keyword matches.
11. For emerging or niche industries, choose the category that best aligns with the core business function, even if it's not a perfect fit.

## Analysis Process:

1. Content Understanding:
   - Identify the main business activities described
   - Determine the primary products or services offered
   - Consider the target market or customers
   - Assess the overall industry or sector the business operates in
   - For multiple business lines, identify which appears to be the most dominant

2. Vertical Matching:
   - Compare the identified business characteristics to each vertical summary
   - Look for the closest matches in terms of activities, products/services, and industry focus
   - Consider both explicit mentions and implied characteristics

3. Context Evaluation:
   - Assess how well the company's overall context aligns with each potential category
   - Consider factors like business model (B2B, B2C, etc.), revenue sources, and unique aspects of the business
   - For emerging or niche industries, focus on the fundamental business function

4. Keyword Analysis:
   - Identify the presence of keywords from each tier in the company information
   - Consider the frequency and context of these keywords
   - Be cautious of negative keywords and evaluate their context
   - Use the keyword presence to support your category selection and confidence assessment
   - Remember that overall business context takes precedence over keyword matches

5. Conflict Resolution:
   - If you encounter conflicting information, prioritize the most reliable and recent data
   - Consider the source and context of conflicting information
   - Make a judgment based on the overall business description rather than isolated details

6. Current Category Evaluation (if provided):
   - Compare your analysis results with the provided current category
   - Determine if you agree or disagree with the current categorization
   - Provide reasoning for your agreement or disagreement

## Output Format:

Provide your analysis in the following format:

PRIMARY_CATEGORY: [Best matching category]

SECONDARY_CATEGORY: [Second-best matching category]

CONFIDENCE: [High/Medium/Low] 

CONFIDENCE_JUSTIFICATION: [Justify your confidence level based on the alignment with vertical description, presence and distribution of keywords from different tiers, and overall business context.]

EXPLANATION: [3-4 sentences explaining your categorization decision. Reference specific details from the company information that support your choice, and explain how these align with the chosen vertical summaries.]

REASONING: [Provide a brief overview of why other potential categories were not chosen, if relevant. Address any conflicting information or multiple business lines if applicable.]

CURRENT_CATEGORY_EVALUATION: [If a current category was provided, state whether you agree or disagree with it and explain why.]

## Example Output:

PRIMARY_CATEGORY: Software & Technology

SECONDARY_CATEGORY: Professional Services

CONFIDENCE: High

CONFIDENCE_JUSTIFICATION: The categorization is based on strong alignment with the Software & Technology vertical description, supported by multiple Tier 1 keywords (e.g., "cloud computing", "SaaS") and clear business focus on software development and IT services.

EXPLANATION: The company primarily develops and provides cloud-based software solutions for businesses, which aligns closely with the Software & Technology vertical. Their product offerings include SaaS platforms for data analytics and customer relationship management, further supporting this categorization. The secondary category of Professional Services reflects their consulting and implementation services that complement their software products.

REASONING: While the company also offers some professional services, these appear to be in support of their core software products rather than the primary focus of the business. Other categories like Manufacturing or Retail were not considered due to the clear emphasis on software development and digital services.

CURRENT_CATEGORY_EVALUATION: The current category of "IT Services" is close but not as precise as Software & Technology. While IT Services is a component of their offering, the primary focus on software development and SaaS products makes Software & Technology a more accurate primary category.

## Final Check:
Before submitting your response, verify that you have:
1. Thoroughly considered the entire company description
2. Matched the company's activities and focus to the provided vertical summaries
3. Only selected categories from the Acceptable Business Industries list
4. Provided a clear explanation referencing specific details from the company information
5. Explained your reasoning, including why other categories were not chosen if relevant
6. Justified your confidence level based on vertical alignment, keyword analysis, and business context
7. Evaluated the current category (if provided) and explained your agreement or disagreement
8. Addressed any conflicting information or multiple business lines (if applicable)
9. Considered whether the business might be an emerging or niche industry not perfectly captured by existing categories

If the company information is too vague or doesn't clearly align with any category, select 'General Business' as the primary category and explain why in your reasoning. If you feel you need more information to make a confident categorization, state this clearly in your response.
"""

    return full_prompt


def format_vertical_summaries(vertical_summaries):
  formatted_text = ""
  for vertical, details in vertical_summaries.items():
    formatted_text += f"### -- {vertical}: -- ###\n"  # Add a space after the hash
    formatted_text += f"\n## Vertical Summary: ##\n{details['vertical_summary']}\n"  # Add a newline before Vertical Summary
    formatted_text += f"## Qualifying Criteria: ##\n{details['qualifying_criteria']}\n\n"
    formatted_text += f"## Keywords: ##\n"
    for tier, keywords in details['keywords'].items():
      formatted_text += f"**{tier.upper()}**: {', '.join(keywords)}\n"
    formatted_text += "\n"
  return formatted_text 

# Llama 3.1 405B - ocid1.generativeaimodel.oc1.us-chicago-1.amaaaaaask7dceyarleil5jr7k2rykljkhapnvhrqvzx4cwuvtfedlfxet4q
# Command R+ - ocid1.generativeaimodel.oc1.us-chicago-1.amaaaaaask7dceya7ozidbukxwtun4ocm4ngco2jukoaht5mygpgr6gq2lgq
# Command R - ocid1.generativeaimodel.oc1.us-chicago-1.amaaaaaask7dceyawk6mgunzodenakhkuwxanvt6wo3jcpf72ln52dymk4wq

def prepare_chat_request(prompt, chat_history, is_url_processing):
    chat_detail = ChatDetails()
    chat_request = CohereChatRequest()
    chat_request.message = prompt
    chat_request.chat_history = chat_history
    chat_request.max_tokens = MAX_TOKENS
    chat_request.temperature = TEMPERATURE
    chat_request.frequency_penalty = FREQUENCY_PENALTY
    chat_request.top_p = TOP_P
    chat_request.top_k = TOP_K
    chat_request.is_stream = True  
    chat_detail.serving_mode = OnDemandServingMode(
        model_id=OCI_MODEL_ID
    )
    chat_detail.chat_request = chat_request
    chat_detail.compartment_id = OCI_COMPARTMENT_ID
    return chat_detail, prompt


def send_chat_request(generative_ai_inference_client, chat_detail, prompt):
    logger.info("Sending request to OCI GenAI Service...")
    logger.info(f"Prompt sent to GenAI service:\n{prompt}")
    start_time = time.time()
    try:
        chat_response = generative_ai_inference_client.chat(chat_detail)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"AI response received in {elapsed_time:.2f} seconds.")
        return chat_response
    except Exception as e:
        logger.error(f"Error in OCI GenAI Service request: {str(e)}")
        return None

def process_streaming_response(chat_response):
    for event in chat_response.data.events():
        res = json.loads(event.data)
        if 'finishReason' in res.keys():
            logger.info(f"Finish reason: {res['finishReason']}")
            yield None  # Signal end of stream
        if 'text' in res:
            yield res['text']

def extract_category(response, category_type):
    match = re.search(rf"{category_type.upper()}_CATEGORY:\s*(.*?)(?=\n|$)", response, re.IGNORECASE)
    return match.group(1).strip() if match else 'N/A'

def extract_confidence(response):
    match = re.search(r'CONFIDENCE:\s*(.*?)(?=\n|$)', response, re.IGNORECASE)
    return match.group(1).strip() if match else 'N/A'

def extract_explanation(response):
    match = re.search(r'EXPLANATION:\s*(.*?)(?=\n|$)', response, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else 'N/A'

def extract_current_category_evaluation(response):
    match = re.search(r'CURRENT_CATEGORY_EVALUATION:\s*(.*?)(?=\n|$)', response, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else 'N/A'

def extract_confidence_justification(response):
    match = re.search(r'CONFIDENCE_JUSTIFICATION:\s*(.*?)(?=\n|$)', response, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else 'N/A'

def validate_category(category, category_type):
    if category not in VALID_CATEGORIES:
        logger.warning(f"Invalid {category_type} category '{category}' returned by AI. Defaulting to 'NEEDS FURTHER REVIEW'.")
        return "NEEDS FURTHER REVIEW" if category_type == "primary" else "N/A"
    return category

def validate_confidence(confidence):
    if confidence not in ["High", "Medium", "Low", "N/A"]:
        logger.warning(f"Invalid confidence level '{confidence}' returned by AI. Defaulting to 'N/A'.")
        return "N/A"
    return confidence

@error_handler
def process_ai_response(response):
    result = {
        'Primary Category': 'NEEDS FURTHER REVIEW',
        'Secondary Category': 'N/A',
        'Confidence': 'N/A',
        'Explanation': '',
        'Confidence Justification': ''
    }

    result['Primary Category'] = validate_category(extract_category(response, "primary"), "primary")
    result['Secondary Category'] = validate_category(extract_category(response, "secondary"), "secondary")
    result['Confidence'] = validate_confidence(extract_confidence(response))
    result['Explanation'] = extract_explanation(response)
    result['Confidence Justification'] = extract_confidence_justification(response)

    return result

def error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            return {
                'Category': 'NEEDS FURTHER REVIEW',
                'Confidence': 'N/A',
                'Explanation': f"Error occurred: {str(e)}"
            }
    return wrapper

@error_handler
def get_ai_response(url, chat_history, customer, webpage_content, relevant_data, generative_ai_inference_client):
    process_id = uuid.uuid4()
    logger.info(f"Processing AI response for URL: {url} (Process ID: {process_id})")
    
    if not url or not isinstance(url, str):
        logger.warning(f"Invalid URL input, skipping AI processing (Process ID: {process_id})")
        yield {
            'Primary Category': 'N/A',
            'Secondary Category': 'N/A',
            'Confidence': 'N/A',
            'Explanation': 'INVALID URL',
            'Confidence Justification': 'N/A'
        }
        return
    
    normalized_url = url
    
    # Process the webpage_content dictionary
    key_content = {
        'source': 'website',
        'home': {
            'summary': extract_key_content(webpage_content.get('home', '')),
            'top_keywords': extract_top_keywords(webpage_content.get('home', ''))
        },
        'about': {
            'summary': extract_key_content(webpage_content.get('about', '')),
            'top_keywords': extract_top_keywords(webpage_content.get('about', ''))
        },
        'combined_keywords': extract_top_keywords(webpage_content.get('home', '') + ' ' + webpage_content.get('about', '')),
        'product_exists': 'products' in webpage_content or 'services' in webpage_content
    }
    
    content_source = 'website'
    prompt = f"Content source: {content_source}\n" + construct_prompt(key_content, customer, relevant_data)

    logger.info(f"Preparing chat request... (Process ID: {process_id})")
    chat_detail, prompt = prepare_chat_request(prompt, chat_history, True)
    
    logger.info(f"Sending chat request to AI service... (Process ID: {process_id})")
    chat_response = send_chat_request(generative_ai_inference_client, chat_detail, prompt)
    
    if chat_response is None:
        logger.error(f"Failed to get response from OCI GenAI Service (Process ID: {process_id})")
        yield {
            'Primary Category': 'NEEDS FURTHER REVIEW',
            'Secondary Category': 'N/A',
            'Confidence': 'N/A',
            'Explanation': 'Error: Failed to get response from OCI GenAI Service',
            'Confidence Justification': 'N/A'
        }
        return

    logger.info(f"Processing streaming AI response... (Process ID: {process_id})")
    full_response = ""
    for chunk in process_streaming_response(chat_response):
        if chunk is None:
            logger.info(f"End of streaming response (Process ID: {process_id})")
            break
        full_response += chunk
        logger.info(f"Yielding chunk: {chunk[:50]}...")  # Log first 50 characters of each chunk
        yield chunk

    logger.info(f"Processing AI response... (Process ID: {process_id})")
    processed_response = process_ai_response(full_response)
    
    logger.info(f"AI response processed. Primary Category: {processed_response['Primary Category']} (Process ID: {process_id})")
    
    yield processed_response

def extract_top_keywords(text, num_keywords=10):
    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalnum() and word not in stop_words]
    
    # Count word frequencies
    word_freq = Counter(words)
    
    # Get top keywords
    top_keywords = [word for word, _ in word_freq.most_common(num_keywords)]
    
    return top_keywords
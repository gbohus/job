from url_utils import normalize_url, extract_url_from_input
from utils import error_handler
from webscraper import get_website_content
from ai_interaction import get_ai_response
from csv_processing import process_csv
import logging
import pandas as pd

logger = logging.getLogger(__name__)

# Add the guidance_prompt here
guidance_prompt = """You are a helpful AI assistant tasked with categorizing businesses based on their website content."""

@error_handler
def categorize_business(url_input, company_info, generative_ai_inference_client, chat_history):
    logger.info(f"Starting categorization for URL: {url_input}")
    url = extract_url_from_input(url_input)
    if url:
        normalized_url = normalize_url(url)
        if not normalized_url.startswith(('http://', 'https://')):
            normalized_url = 'https://' + normalized_url
        logger.info(f"Extracted and normalized URL: {normalized_url}")
        webpage_content = get_website_content(normalized_url, company_info)
        
        relevant_data = {
            'Customer': company_info,
            'Maximum of City': '',
            'Maximum of Country': '',
            'Maximum of State/Province': '',
            'Web Address': normalized_url
        }
        
        logger.info("Sending request to AI for categorization")
        for chunk in get_ai_response(normalized_url, chat_history, company_info, webpage_content, relevant_data, generative_ai_inference_client):
            if isinstance(chunk, dict):
                logger.info(f"Yielding final response: {chunk}")
            else:
                logger.info(f"Yielding chunk from get_ai_response: {chunk[:50] if isinstance(chunk, str) else 'Non-string chunk'}...")
            yield chunk
    else:
        logger.warning("No valid URL detected.")
        yield {
            'Primary Category': 'N/A',
            'Secondary Category': 'N/A',
            'Confidence': 'N/A',
            'Explanation': 'NO URL FOUND',
            'Confidence Justification': 'N/A'
        }
    logger.info("categorize_business completed")

def process_csv_file(input_file, output_file, generative_ai_inference_client, compartment_id, progress_callback=None):
    logger.info(f"Processing input file: {input_file}")
    logger.info(f"Output will be saved to: {output_file}")
    
    # Step 1: Reading file
    if progress_callback:
        progress_callback(0)
    
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        logger.error(f"Error reading CSV file: {str(e)}")
        raise ValueError(f"Unable to read the CSV file. Error: {str(e)}")
    
    if df.empty:
        raise ValueError("The input CSV file is empty.")
    
    required_columns = ['Customer', 'Web Address']  # Add any other required columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"The following required columns are missing: {', '.join(missing_columns)}")
    
    total_rows = len(df)
    logger.info(f"Total rows to process: {total_rows}")
    
    process_csv(input_file, output_file, generative_ai_inference_client, compartment_id, progress_callback)
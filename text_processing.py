import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
import logging 
import string

logger = logging.getLogger(__name__)

def preprocess_content(content):
    try:
        # Check if content is a string
        if not isinstance(content, str):
            content = str(content)

        # Remove URLs
        content = re.sub(r'http\S+|www\S+|https\S+', '', content, flags=re.MULTILINE)
        
        # Remove email addresses
        content = re.sub(r'\S*@\S*\s?', '', content)
        
        # Remove extra whitespace
        content = ' '.join(content.split())
        
        return content
    except Exception as e:
        logger.error(f"Error in preprocess_content: {str(e)}")
        return str(content)  # Return string representation as fallback

def extract_key_content(text, max_words=50000):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    # Tokenize words and remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for sentence in sentences for word in word_tokenize(sentence) 
             if word.lower() not in stop_words and word not in string.punctuation]

    # Get the most common words
    word_freq = nltk.FreqDist(words)
    most_common = word_freq.most_common(max_words)

    # Reconstruct the text using sentences containing the most common words
    key_sentences = []
    for sentence in sentences:
        if any(word[0] in sentence.lower() for word in most_common):
            key_sentences.append(sentence)

    # Join the key sentences
    key_content = ' '.join(key_sentences)

    # Truncate to max_words if necessary
    words = key_content.split()
    if len(words) > max_words:
        key_content = ' '.join(words[:max_words])

    return key_content

def extract_business_model_indicators(webpage_content):
    indicators = []
    content = webpage_content.get('home', '') + ' ' + webpage_content.get('about', '')
    content = content.lower()
    
    if 'b2b' in content or 'business to business' in content:
        indicators.append('B2B')
    if 'b2c' in content or 'business to consumer' in content:
        indicators.append('B2C')
    if 'non-profit' in content or 'nonprofit' in content or '501(c)3' in content:
        indicators.append('Non-profit')
    if 'e-commerce' in content or 'online store' in content:
        indicators.append('E-commerce')
    if 'wholesale' in content:
        indicators.append('Wholesale')
    if 'manufacturer' in content or 'manufacturing' in content:
        indicators.append('Manufacturing')
    
    return indicators
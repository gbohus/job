import re
import validators
import logging

logger = logging.getLogger(__name__)

def normalize_url(url):
    # Remove 'http://' or 'https://' from the beginning of the URL
    url = re.sub(r'^https?://', '', url)
    
    # Remove 'www.' if it exists
    url = re.sub(r'^www\.', '', url)
    
    # Remove trailing slash if it exists
    url = url.rstrip('/')
    
    # Add 'https://' to the beginning of the URL
    url = 'https://' + url
    
    return url

def extract_url_from_input(input_text):
    # First, try to find a URL with http:// or https://
    url_pattern = re.compile(r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)')
    matches = url_pattern.findall(input_text)
    if matches:
        return matches[-1]
    
    # If no match, try to find a domain-like string
    domain_pattern = re.compile(r'(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)')
    matches = domain_pattern.findall(input_text)
    if matches:
        return 'https://' + matches[-1]
    
    return None

def is_valid_url(url):
    try:
        result = validators.url(url)
        logger.info(f"URL validation result for {url}: {result}")
        if not result:
            # If validation fails, try prepending 'http://' and validate again
            result = validators.url('http://' + url)
            logger.info(f"Second URL validation result for http://{url}: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in URL validation for {url}: {str(e)}")
        return False
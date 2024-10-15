import requests
import logging
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import gzip
import zlib
import brotli
import chardet
from url_utils import is_valid_url
from utils import error_handler
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import io

logger = logging.getLogger(__name__)

def score_link(link_text, link_href):
    score = 0
    
    # Keywords in link text
    about_keywords = ['about', 'about us', 'who we are', 'our story', 'mission', 'vision', 'values', 'team', 'company']
    product_keywords = ['product', 'products', 'solutions', 'services', 'offerings']
    
    for keyword in about_keywords:
        if keyword in link_text.lower():
            score += 2
        if keyword in link_href.lower():
            score += 1
    
    for keyword in product_keywords:
        if keyword in link_text.lower():
            score += 2
        if keyword in link_href.lower():
            score += 1
    
    # Prefer shorter URLs
    if len(link_href.split('/')) <= 2:
        score += 1
    
    # Avoid links to external sites or irrelevant sections
    avoid_keywords = ['contact', 'blog', 'news', 'careers', 'jobs', 'login', 'sign']
    if any(keyword in link_href.lower() for keyword in avoid_keywords):
        score -= 2
    
    return score


def find_pages(base_url):
    try:
        if not base_url.startswith(('http://', 'https://')):
            base_url = 'https://' + base_url

        logger.info(f"Identifying pages from base URL: {base_url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate'
        }
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        logger.info(f"Response status code: {response.status_code}")

        if response.status_code == 403:
            logger.error(f"403 Forbidden error for URL: {base_url}")
            return {'home': base_url, 'about': None, 'product': None}

        content = response.content

        # Handle various content encodings
        content_encoding = response.headers.get('Content-Encoding', '').lower()
        if content_encoding:
            try:
                if 'gzip' in content_encoding:
                    try:
                        content = gzip.decompress(content)
                    except IOError:
                        # If gzip decompression fails, try to read it as plain text
                        content = io.BytesIO(content).read()
                        logger.debug("Failed to decompress gzip content, proceeding with raw content.")
                elif 'deflate' in content_encoding:
                    content = zlib.decompress(content)
                elif 'br' in content_encoding:
                    content = brotli.decompress(content)
            except Exception as e:
                logger.debug(f"Failed to decompress content ({content_encoding}): {e}")
                logger.debug("Proceeding with raw content.")

        # Try to detect the encoding
        encoding = response.encoding
        if encoding is None or encoding.lower() == 'iso-8859-1':
            detected = chardet.detect(content)
            encoding = detected['encoding']

        # Decode the content with the detected encoding, falling back to UTF-8 if necessary
        try:
            decoded_content = content.decode(encoding or 'utf-8', errors='replace')
        except (UnicodeDecodeError, LookupError):
            logger.warning(f"Failed to decode content with detected encoding {encoding}. Falling back to UTF-8.")
            decoded_content = content.decode('utf-8', errors='replace')

        soup = BeautifulSoup(decoded_content, 'html.parser')
        
        scored_links = []
        
        # Add the home page with a high score
        scored_links.append((base_url, 100, "Home"))
        
        logger.info("All links found on the page:")
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith(('http://', 'https://', '//', 'www')):
                if urlparse(base_url).netloc not in href:
                    continue
            else:
                href = urljoin(base_url, href)
            
            score = score_link(link.text, href)
            scored_links.append((href, score, link.text))
            logger.info(f"Link: {href}, Text: {link.text}, Score: {score}")
        
        scored_links.sort(key=lambda x: x[1], reverse=True)
        
        logger.info("Top scored links:")
        for href, score, text in scored_links[:10]:
            logger.info(f"URL: {href}, Text: {text}, Score: {score}")
        
        pages = {
            'home': base_url,
            'about': None,
            'product': None
        }
        
        for href, score, text in scored_links:
            if not pages['about'] and ('about' in href.lower() or 'about' in text.lower()):
                pages['about'] = href
            elif not pages['product'] and ('product' in href.lower() or 'product' in text.lower()):
                pages['product'] = href
            
            if pages['about'] and pages['product']:
                break
        
        logger.info(f"Final identified pages: {pages}")
        return pages
    
    except Exception as e:
        logger.error(f"Error finding pages: {e}")
        return {'home': base_url, 'about': None, 'product': None}


def fetch_webpage_content(url):
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
    ]
    
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.google.com/'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        if response.status_code == 403:
            logger.error(f"403 Forbidden error for URL: {url}")
            return f"Sorry, access to this website ({url}) is forbidden. The site may have anti-scraping measures in place."

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for element in soup(['script', 'style']):
            element.decompose()
        
        # Extract text from the entire page
        text_content = soup.get_text(separator='\n', strip=True)
        
        # Remove extra whitespace
        text_content = re.sub(r'\s+', ' ', text_content).strip()

        logger.info(f"Content extracted from {url}. Length: {len(text_content)}")
        
        # Log the actual content (limited to first 100000 characters to avoid extremely large logs)
        logger.info(f"Extracted content from {url} (first 100000 chars): {text_content[:100000]}")

        return text_content[:100000] + ("..." if len(text_content) > 100000 else "")
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch content from {url}: {str(e)}")
        return f"Sorry, I couldn't fetch the content from the webpage {url}. Error: {str(e)}"
    
    except Exception as e:
        logger.error(f"An unexpected error occurred while processing {url}: {e}")
        return f"An unexpected error occurred while processing the webpage {url}. Error: {str(e)}"


@error_handler
def get_website_content(url, company_info):
    logger.info(f"Fetching website content for URL: {url}")
    pages = find_pages(url)
    content = {'home': 'N/A', 'about': 'N/A', 'product_exists': False, 'source': 'N/A'}

    logger.info(f"Pages found: {pages}")

    logger.info("=" * 80)
    logger.info(f"Attempting to scrape pages for URL: {url}")
    logger.info("=" * 80)

    content_found = False

    with requests.Session() as session:
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        with ThreadPoolExecutor(max_workers=20) as executor:
            future_to_page = {executor.submit(fetch_webpage_content, pages.get(page_type)): page_type 
                              for page_type in ['home', 'about'] if pages.get(page_type)}

            for future in as_completed(future_to_page):
                page_type = future_to_page[future]
                try:
                    page_content = future.result()
                    logger.info(f"Content received for {page_type}: {bool(page_content)}")
                    if page_content and not page_content.startswith("Sorry,") and not page_content.startswith("An unexpected error"):
                        content[page_type] = page_content
                        content_found = True
                        logger.info(f"{page_type.capitalize()} content length: {len(content[page_type])}")
                        logger.debug(f"{page_type.capitalize()} content (first 1000 chars): {content[page_type][:1000]}")
                    else:
                        logger.warning(f"Failed to fetch content for {page_type} page: {page_content}")
                except Exception as exc:
                    logger.error(f"Exception when scraping {page_type} page: {exc}")

    content['product_exists'] = bool(pages.get('product'))

    if not content_found:
        logger.warning(f"No content found for URL: {url}")
        logger.info("Falling back to DuckDuckGo search...")
        search_content = duckduckgo_search(company_info)
        if search_content:
            content['home'] = search_content
            content['source'] = 'web_search'
            logger.info(f"DuckDuckGo search fallback successful. Content length: {len(search_content)}")
        else:
            logger.warning("DuckDuckGo search fallback failed.")
    else:
        content['source'] = 'website'

    return content


def duckduckgo_search(company_info, num_results=5):
    query = f"{company_info} company information"
    url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find_all('div', class_='result__body')
        
        search_results = []
        for result in results[:num_results]:
            title = result.find('a', class_='result__a').text
            snippet = result.find('a', class_='result__snippet').text
            search_results.append(f"{title}\n{snippet}\n\n")
        
        return ' '.join(search_results)
    except Exception as e:
        logger.error(f"Error in DuckDuckGo search: {str(e)}")
        return ""
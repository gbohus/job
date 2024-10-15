import logging
import oci
from oci.config import from_file
import functools
from url_utils import normalize_url, extract_url_from_input, is_valid_url
from config import OCI_CONFIG_PROFILE, OCI_COMPARTMENT_ID

logger = logging.getLogger(__name__)

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

def setup_oci_client(config_profile=OCI_CONFIG_PROFILE):
    config = from_file('~/.oci/config', config_profile)
    endpoint = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"
    generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(config=config, service_endpoint=endpoint, retry_strategy=oci.retry.NoneRetryStrategy(), timeout=(10,240))

    return generative_ai_inference_client
import logging
import os
import nltk
from logging.handlers import RotatingFileHandler
from config import LOG_FILE, LOG_LEVEL

def setup_nltk():
    nltk_data_dir = os.path.expanduser('~/.nltk_data')
    os.makedirs(nltk_data_dir, exist_ok=True)
    nltk.data.path.append(nltk_data_dir)

    required_resources = ['punkt', 'stopwords', 'averaged_perceptron_tagger']
    for resource in required_resources:
        try:
            nltk.download(resource, download_dir=nltk_data_dir, quiet=True)
        except Exception as e:
            logging.error(f"Failed to download NLTK resource {resource}: {str(e)}")

def setup_logging(log_file=LOG_FILE, log_level=LOG_LEVEL):
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    # File handler with rotation
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    # Remove all existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
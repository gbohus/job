from setup_utils import setup_nltk, setup_logging
from utils import setup_oci_client
from core_logic import categorize_business, process_csv_file, guidance_prompt  # Import guidance_prompt
import os
import uuid
import sys

# Setup NLTK
setup_nltk()

# Initialize logger
logger = setup_logging()

# Global flag to prevent multiple executions
EXECUTION_FLAG = False

def main():
    global EXECUTION_FLAG
    if EXECUTION_FLAG:
        logger.warning("Application is already running. Exiting duplicate execution.")
        return
    EXECUTION_FLAG = True

    try:
        logger.info("OCI AI-powered Business Categorizer")
        logger.info("1. Interactive chat")
        logger.info("2. Process CSV file")
        
        while True:
            choice = input("Enter your choice (1 or 2): ").strip()
            if choice in ['1', '2']:
                break
            logger.warning("Invalid choice. Please enter 1 or 2.")
            
        compartment_id = "ocid1.compartment.oc1..aaaaaaaaaf25ldyl5rxegseg4h4m2tpbvnecoh7w4tb5uisql2uhq32abrra"
        CONFIG_PROFILE = "DEFAULT"

        generative_ai_inference_client = setup_oci_client(CONFIG_PROFILE)

        if choice == '1':
            interactive_chat(generative_ai_inference_client)
        elif choice == '2':
            process_csv_mode(generative_ai_inference_client, compartment_id)
        
        logger.info("Process completed. Thank you for using the Business Categorizer!")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
    finally:
        EXECUTION_FLAG = False

def process_csv_mode(generative_ai_inference_client, compartment_id):
    while True:
        input_file = input("Enter the input CSV file path (or 'back' to return to main menu): ").strip()
        if input_file.lower() == 'back':
            return

        input_file = input_file.lstrip('& ').strip("'\"")
        input_file = os.path.normpath(input_file)
        
        if os.path.exists(input_file):
            break
        logger.error(f"File not found: {input_file}")
    
    input_file_name = os.path.basename(input_file)
    file_name, file_extension = os.path.splitext(input_file_name)
    output_file = os.path.join(os.path.dirname(input_file), f"{file_name}_results{file_extension}")
    
    process_csv_file(input_file, output_file, generative_ai_inference_client, compartment_id)

def interactive_chat(generative_ai_inference_client):
    logger.info("Welcome to the interactive chat mode!")
    logger.info("You can categorize businesses by entering a URL and company information.")
    logger.info("Type 'quit' to exit the chat mode or 'back' to return to the main menu.")
    
    chat_history = [{'role': "SYSTEM", 'message': guidance_prompt}]
    
    while True:
        url_input = input("\nEnter a URL (or 'quit' to exit, 'back' for main menu): ").strip()
        
        if url_input.lower() == 'quit':
            logger.info("Exiting interactive chat mode. Goodbye!")
            break
        elif url_input.lower() == 'back':
            return
        
        if not url_input:
            logger.warning("URL cannot be empty. Please try again.")
            continue
        
        company_info = input("Enter the company name and address: ").strip()
        
        if not company_info:
            logger.warning("Company information cannot be empty. Please try again.")
            continue
        
        current_category = input("Enter the current category (if known, otherwise press Enter): ").strip()
        
        process_id = uuid.uuid4()
        logger.info(f"Sending request to AI for URL: {url_input} (Process ID: {process_id})")
        response, normalized_url = categorize_business(url_input, company_info, current_category, generative_ai_inference_client, chat_history)
        logger.info(f"Received AI response for URL: {url_input} (Process ID: {process_id})")
        
        print("\nJob Routing Classification:")
        print("=" * 50)
        print(f"Primary Category: {response['Primary Category']}")
        print(f"Secondary Category: {response['Secondary Category']}")
        print(f"Confidence: {response['Confidence']}")
        print(f"\nExplanation: {response['Explanation']}")
        print(f"\nConfidence Justification: {response['Confidence Justification']}")
        print(f"\nCurrent Category Evaluation: {response['Current Category Evaluation']}")
        print("=" * 50)
        
        # Update chat history
        chat_history.append({'role': "USER", 'message': f"URL: {url_input}, Company Info: {company_info}, Current Category: {current_category}"})
        chat_history.append({'role': "CHATBOT", 'message': str(response)})

if __name__ == "__main__":
    main()
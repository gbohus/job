import csv
import os
import logging
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from ai_interaction import get_ai_response, process_ai_response
from webscraper import get_website_content
from text_processing import extract_key_content
from utils import setup_oci_client

logger = logging.getLogger(__name__)


def process_row(row, generative_ai_inference_client, chat_history):
    # Define the fields we want to consider
    relevant_fields = ['Customer', 'Maximum of City', 'Maximum of Country', 'Maximum of State/Province', 'Web Address', 'CS Sales LOB']
    
    # Create a new dictionary with only the relevant fields
    relevant_data = {field: row.get(field, '') for field in relevant_fields}
    
    url = relevant_data.get('Web Address', '')
    customer = relevant_data.get('Customer', '')
    cs_sales_lob = relevant_data.get('CS Sales LOB', '')

    if not url:
        logger.warning(f"No URL found for customer: {customer}")
        return {
            **row, 
            'Primary Category': 'N/A', 
            'Secondary Category': 'N/A',
            'Confidence': 'N/A', 
            'Explanation': f'NO URL FOUND for {customer}',
            'Confidence Justification': 'N/A',
            'Match?': 'N/A'
        }

    try:
        logger.info(f"Processing customer: {customer} with URL: {url}")

        # Get website content
        webpage_content = get_website_content(url, customer)  

        if not webpage_content:
            logger.warning(f"No content retrieved for {customer} (URL: {url})")
            return {
                **row, 
                'Primary Category': 'No Content', 
                'Secondary Category': 'N/A',
                'Confidence': 'N/A', 
                'Explanation': f'Unable to retrieve content for {customer} (URL: {url})',
                'Confidence Justification': 'N/A',
                'Match?': 'N/A'
            }
        
        # Call get_ai_response without current_category
        ai_response = None
        for chunk in get_ai_response(url, chat_history, customer, webpage_content, relevant_data, generative_ai_inference_client):
            if isinstance(chunk, dict):
                ai_response = chunk
                break

        if ai_response is None:
            raise ValueError("No valid response received from AI")

        primary_category = ai_response.get('Primary Category', 'N/A')
        match = 'Yes' if primary_category.lower() == cs_sales_lob.lower() else 'No'

        return {
            **row,
            'Primary Category': primary_category,
            'Secondary Category': ai_response.get('Secondary Category', 'N/A'),
            'Confidence': ai_response.get('Confidence', 'N/A'),
            'Explanation': ai_response.get('Explanation', 'N/A'),
            'Confidence Justification': ai_response.get('Confidence Justification', 'N/A'),
            'Match?': match
        }
    except Exception as e:
        logger.error(f"Error processing row for {customer} (URL: {url}): {str(e)}", exc_info=True)
        return {
            **row, 
            'Primary Category': 'Error', 
            'Secondary Category': 'N/A',
            'Confidence': 'N/A', 
            'Explanation': f'Error processing {customer} (URL: {url}): {str(e)}',
            'Confidence Justification': 'N/A',
            'Match?': 'N/A'
        }


def process_csv(input_file, output_file, generative_ai_inference_client, compartment_id, progress_callback=None):
    logger.info(f"Processing CSV file: {input_file}")
    logger.info(f"Output will be saved to: {output_file}")
    
    # Step 1: Reading file
    if progress_callback:
        progress_callback(0)
    
    df = pd.read_csv(input_file)
    
    # Validate headers (keep your existing validation code here)
    
    total_rows = len(df)
    logger.info(f"Total rows to process: {total_rows}")
    
    results = []
    
    # Step 2: Reading Websites
    if progress_callback:
        progress_callback(1)
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_row, row.to_dict(), generative_ai_inference_client, []) for _, row in df.iterrows()]
        
        # Step 3: Sending to GenAI
        if progress_callback:
            progress_callback(2)
        
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
                logger.info(f"Processed row {len(results)}/{total_rows}: {result['Customer']} - {result['Primary Category']}")
            except Exception as exc:
                logger.error(f"Row {len(results) + 1} generated an exception: {exc}")
    
    # Step 4: Reading Results
    if progress_callback:
        progress_callback(3)
    
    results_df = pd.DataFrame(results)
    
    # Step 5: Creating CSV
    if progress_callback:
        progress_callback(4)
    
    # Write results to output file
    results_df.to_csv(output_file, index=False)
    
    logger.info(f"CSV processing completed. Output saved to: {output_file}")    
    # Step 6: Complete
    if progress_callback:
        progress_callback(5)

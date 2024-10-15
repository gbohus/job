import streamlit as st
from PIL import Image
from setup_utils import setup_nltk, setup_logging
from utils import setup_oci_client, error_handler
from core_logic import categorize_business, process_csv_file, guidance_prompt
import os
import logging
from config import OCI_CONFIG_PROFILE, OCI_COMPARTMENT_ID
import pandas as pd
import uuid
import re
import time
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import networkx as nx
import base64

# Load your icon image
icon = Image.open('Logo/NetSuite logo - Icon.png')

# Add this near the top of your file, after the imports
st.set_page_config(
    page_title="AI Powered Job Routing",
    page_icon=icon,

)

def set_background_image(image_file, x_position='center', y_position='center'):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: {x_position} {y_position};
        background-size: cover;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
    .main .block-container {{
        background-color: white;
        padding: 3rem;
        border-radius: 30px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        max-width: 760px;
        margin: auto;
        margin-top: 80px;
    }}
    header {{
        background-color: #264759 !important;
    }}
    .stDeployButton {{
        display: none !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

def main():
    try:
          set_background_image('Logo/Background_logo.png', x_position='0px', y_position='-500px')
    except Exception as e:
        st.error(f"Error setting background image: {str(e)}")
    render_ui()

# Setup logging
logger = setup_logging()

# Setup NLTK
setup_nltk()

# Setup OCI client
@st.cache_resource
def get_oci_client():
    return setup_oci_client(OCI_CONFIG_PROFILE)

generative_ai_inference_client = get_oci_client()

# Initialize session state
if 'execution_id' not in st.session_state:
    st.session_state.execution_id = str(uuid.uuid4())
    logger.info(f"New execution started with ID: {st.session_state.execution_id}")

if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False



def render_ui():
    logo = Image.open('Logo/NetSuite logo.png')
    st.image(logo, width=200)
    
    st.header("AI Powered Job Routing")
    # Only show the explanatory text if processing is not complete
    if not st.session_state.get('processing_complete', False):
        with st.expander("Job Routing Overview (Read Me)"):
            st.markdown("""
            #### Job Routing Overview

            This tool is designed to classify businesses based on their website data, primarily from the home page and about page. It also takes into consideration whether the business sells physical products. 
                        
            All of this information is then fed into an advanced AI system that analyzes the collected data and compares it against NetSuite's industry alignments.

                        
            **The classification process involves:**
            1. Analyzing the content of the business website
            2. Evaluating the primary business activities and offerings
            3. Considering the presence of physical products in the business model

                        
            **AI system determination:**
            """)
            
            # Display a smaller AI Decision Process image
            ai_decision_process = Image.open('Logo/chart.png')
            st.image(ai_decision_process, caption='AI Decision Process', width=400)

            st.markdown("""
            Based on this analysis, the AI determines which NetSuite vertical would best serve the business, providing a tailored recommendation for their enterprise software needs.

            ---
            """)

    # Create tabs
    tab1, tab2 = st.tabs(["Single Job Classification", "Multiple Job Classification"])

    with tab1:
        st.subheader("Single Job Classification")
        render_interactive_chat()

    with tab2:
        st.subheader("Multiple Job Classification")
        render_process_csv()



def reset_form():
    st.session_state.url_input = ""
    st.session_state.company_info = ""
    st.session_state.form_submitted = False
    st.session_state.processing_complete = False
    if 'result' in st.session_state:
        del st.session_state.result

def render_interactive_chat():
    # Expander for the form
    expander = st.expander("Business Information", expanded=not st.session_state.get('form_submitted', False))
    
    with expander:
        company_info = st.text_input("Enter the company name and address*", 
                                     value=st.session_state.get('company_info', ''),
                                     placeholder="Company Name, Address", 
                                     key="company_info")
        url_input = st.text_input("Enter a URL*", 
                                  value=st.session_state.get('url_input', ''),
                                  placeholder="https://example.com", 
                                  key="url_input")
        
        
        # Create two columns for Submit and Reset buttons
        col1, col2 = st.columns(2)
        with col1:
            submit_button = st.button("Submit", key="submit_button")
        with col2:
            reset_button = st.button("Reset Form", key="reset_button", on_click=reset_form)

    if submit_button and url_input and company_info:
        st.session_state.form_submitted = True
        st.session_state.processing_complete = False
        st.rerun()

    if st.session_state.get('form_submitted', False) and not st.session_state.get('processing_complete', False):
        process_interactive_chat(url_input, company_info)

def process_interactive_chat(url_input, company_info):
    logger.info(f"Starting process_interactive_chat (Execution ID: {st.session_state.execution_id})")
    
    chat_history = [{'role': "SYSTEM", 'message': guidance_prompt}]
    
    # Create placeholders for progress bar, status, streaming, and final result
    progress_bar = st.progress(0)
    status_text = st.empty()
    streaming_placeholder = st.empty()
    separator_placeholder = st.empty()
    result_placeholder = st.empty()
    
    full_response = ""
    status_text.text("Processing... Please wait.")
    
    # Estimate total tokens for progress bar
    estimated_total_tokens = 350  # Adjust this based on your average response length
    tokens_received = 0
    
    try:
        logger.info(f"Calling categorize_business for URL: {url_input}")
        for chunk in categorize_business(url_input, company_info, generative_ai_inference_client, chat_history):
            if isinstance(chunk, dict):
                # This is the final processed response
                response = chunk
                logger.info(f"Received final response: {response}")
                progress_bar.progress(100)
                status_text.text("Processing complete! (100%)")
                separator_placeholder.markdown("---")
                result_placeholder.markdown(f"""
                #### Job Routing Classification:
                
                **Primary Category:** {response.get('Primary Category', 'N/A')}
                
                **Secondary Category:** {response.get('Secondary Category', 'N/A')}
                
                **Confidence:** {response.get('Confidence', 'N/A')}
                
                **Explanation:** {response.get('Explanation', 'N/A')}
                
                **Confidence Justification:** {response.get('Confidence Justification', 'N/A')}
                """)
                # Clear the streaming placeholder
                streaming_placeholder.empty()
            elif isinstance(chunk, str):
                # This is a chunk of the streaming response
                full_response += chunk
                streaming_placeholder.markdown(f"**Job Routing Classification:**\n\n{full_response}")
                
                # Update progress bar and percentage
                tokens_received += len(chunk.split())
                progress = min(tokens_received / estimated_total_tokens, 0.99)
                progress_percentage = int(progress * 100)
                progress_bar.progress(progress)
                status_text.text(f"Processing... {progress_percentage}% complete")
            else:
                logger.warning(f"Received unexpected chunk type: {type(chunk)}")
        
        logger.info(f"Categorization complete (Execution ID: {st.session_state.execution_id})")
    except Exception as e:
        logger.error(f"Error in process_interactive_chat: {str(e)}", exc_info=True)
        status_text.text("An error occurred during processing.")
        result_placeholder.error(f"Error: {str(e)}")
    
    st.session_state.processing_complete = True
    logger.info("process_interactive_chat completed")

def render_process_csv():
    if 'processed_results' not in st.session_state:
        st.session_state.processed_results = None
    if 'output_file_path' not in st.session_state:
        st.session_state.output_file_path = None
    if 'csv_processed' not in st.session_state:
        st.session_state.csv_processed = False

    # Add a reset button
    if st.session_state.csv_processed:
        if st.button("Upload New CSV"):
            st.session_state.csv_processed = False
            st.session_state.processed_results = None
            st.session_state.output_file_path = None
            st.rerun()

    # Put the file uploader and related logic inside an expander
    with st.expander("Upload and Process CSV", expanded=True):
        # Always show the file uploader
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key="csv_uploader")
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                if df.empty:
                    st.error("The uploaded CSV file is empty. Please upload a file with data.")
                    return
                st.write(f"Uploaded file contains {len(df)} rows")
                if st.button("Process CSV", key="process_csv_button"):
                    process_uploaded_csv(uploaded_file)
                    st.rerun()
            except Exception as e:
                handle_csv_upload_error(e)
    
    if st.session_state.csv_processed:
        display_csv_results()

def process_uploaded_csv(uploaded_file):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    def update_progress(step):
        progress_mapping = {0: 0, 1: 20, 2: 40, 3: 60, 4: 80, 5: 100}
        progress = progress_mapping.get(step, 0)
        progress_bar.progress(progress)
        status_messages = [
            "Starting processing...",
            "Reading websites...",
            "Sending to GenAI (Please wait, results will be shown below)...",
            "Reading results...",
            "Creating CSV...",
            "Processing complete! Scroll down to see results."
        ]
        status_text.text(status_messages[step])
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_file = f"output_{timestamp}.csv"
    
    try:
        with open("temp_input.csv", "wb") as f:
            f.write(uploaded_file.getvalue())
        
        process_csv_file("temp_input.csv", output_file, generative_ai_inference_client, OCI_COMPARTMENT_ID, update_progress)
        st.session_state.processed_results = pd.read_csv(output_file)
        st.session_state.output_file_path = output_file
        st.session_state.csv_processed = True
        st.success(f"Processing complete! Output saved as {output_file}")
    except Exception as e:
        st.error(f"An error occurred during processing: {str(e)}")
        logger.error(f"Error in CSV processing: {str(e)}", exc_info=True)
    finally:
        if os.path.exists("temp_input.csv"):
            os.remove("temp_input.csv")

def display_csv_results():
    if st.session_state.output_file_path:
        with open(st.session_state.output_file_path, "rb") as file:
            st.download_button(
                label="Download processed CSV",
                data=file,
                file_name=st.session_state.output_file_path,
                mime="text/csv",
                key="download_csv_button"
            )
    
    if st.session_state.processed_results is not None:
        results_df = st.session_state.processed_results
        
        st.subheader("All Results")
        st.dataframe(results_df)

        # Display high confidence results
        st.subheader("High Confidence Results")
        high_confidence_df = results_df[results_df['Confidence'] == 'High']
        if not high_confidence_df.empty:
            st.dataframe(high_confidence_df)
        else:
            st.info("No results with High confidence found.")

        # Display medium confidence results
        st.subheader("Medium Confidence Results")
        medium_confidence_df = results_df[results_df['Confidence'] == 'Medium']
        if not medium_confidence_df.empty:
            st.dataframe(medium_confidence_df)
        else:
            st.info("No results with Medium confidence found.")

        # Display low confidence results
        st.subheader("Low Confidence Results")
        low_confidence_df = results_df[results_df['Confidence'] == 'Low']
        if not low_confidence_df.empty:
            st.dataframe(low_confidence_df)
        else:
            st.info("No results with Low confidence found.")

        # Display matched results
        st.subheader("Matched to NetSuite Results")
        matched_df = results_df[results_df['Match?'] == 'Yes']
        if not matched_df.empty:
            st.dataframe(matched_df)
        else:
            st.info("No matched results found.")

        # Display unmatched results
        st.subheader("Did Not Match to NetSuite Results")
        unmatched_df = results_df[results_df['Match?'] == 'No']
        if not unmatched_df.empty:
            st.dataframe(unmatched_df)
        else:
            st.info("No unmatched results found.")

        # Add visualizations
        st.subheader("Visualizations")

        # 1. Confidence Distribution Pie Chart
        confidence_counts = results_df['Confidence'].value_counts()
        fig_confidence_pie = px.pie(values=confidence_counts.values, names=confidence_counts.index, title="Confidence Distribution")
        st.plotly_chart(fig_confidence_pie)

        # 2. Match Rate Bar Chart
        match_counts = results_df['Match?'].value_counts()
        fig_match_bar = px.bar(x=match_counts.index, y=match_counts.values, title="Match Rate")
        st.plotly_chart(fig_match_bar)

        # 3. Top Primary Categories
        top_categories = results_df['Primary Category'].value_counts().nlargest(5)
        fig_top_categories = px.bar(
            x=top_categories.values,
            y=top_categories.index,
            orientation='h',
            title="Top 5 Verticals",
            labels={'x': 'Count', 'y': 'Vertical'}  # Adding labels for X and Y axes
        )
        fig_top_categories.update_layout(
            xaxis_title="# of Occurrences",
            yaxis_title="Vertical"
        )
        st.plotly_chart(fig_top_categories)

        # 4. Confidence vs. Match Heatmap
        confidence_match_counts = pd.crosstab(results_df['Confidence'], results_df['Match?'])
        fig_heatmap = px.imshow(confidence_match_counts, title="Confidence vs. Match Heatmap")
        st.plotly_chart(fig_heatmap)


def handle_csv_upload_error(e):
    if isinstance(e, pd.errors.EmptyDataError):
        st.error("The uploaded CSV file is empty. Please upload a file with data.")
    elif isinstance(e, pd.errors.ParserError):
        st.error(f"Unable to parse the CSV file. Error: {str(e)}")
        st.text("Please ensure it's a valid CSV format. Check the file encoding and delimiter.")
    else:
        st.error(f"An error occurred while reading the file: {str(e)}")
        logger.error(f"Error reading CSV file: {str(e)}", exc_info=True)



if __name__ == "__main__":
    main()
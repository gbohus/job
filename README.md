# AI-Powered Job Routing

## Overview
This application is an AI-powered tool designed to categorize businesses based on their website content and company information. It uses advanced natural language processing and machine learning techniques to analyze business data and classify it into appropriate industry verticals, leveraging Oracle Cloud Infrastructure's Generative AI service for accurate categorization.

## Features
- Single Job Classification: Analyze individual businesses by providing a URL and company information.
- Multiple Job Classification: Process multiple businesses at once using a CSV file.
- Interactive Web Interface: User-friendly Streamlit app for easy interaction.
- AI-Powered Analysis: Utilizes Oracle Cloud Infrastructure's Generative AI service for accurate categorization.
- Detailed Explanations: Provides confidence levels and justifications for each classification.
- Web Scraping: Automatically extracts relevant information from company websites.
- CSV Processing: Handles bulk processing of company data from CSV files.
- Visualizations: Includes various charts and graphs to represent classification results.

## Requirements
- Python 3.7+
- Oracle Cloud Infrastructure (OCI) account with access to Generative AI service
- OCI SDK configured on your machine

## Installation

1. Clone the repository:   ```
   git clone https://github.com/your-username/ai-powered-job-routing.git
   cd ai-powered-job-routing   ```

2. Install the required packages:   ```
   pip install -r requirements.txt   ```

3. Set up your OCI configuration file (`~/.oci/config`) with your credentials.

## Configuration

Update the `config.py` file with your OCI details:
- `OCI_CONFIG_PROFILE`: Your OCI config profile (default is 'DEFAULT')
- `OCI_COMPARTMENT_ID`: Your OCI compartment ID
- `OCI_MODEL_ID`: The ID of the OCI AI model you want to use

## Usage

### Running the Streamlit App

To start the web application, run:

# OCI Configuration
    # To modify these settings:
    # Set environment variables with the same names as the variables below,
    # Your OCI config profile (usually 'DEFAULT' unless you've set up multiple profiles)
    # Your OCI compartment ID (replace with your own)
    # The ID of the OCI AI model you want to use (replace with your preferred model), only works with Command R/R+
#################### OCI_CONFIG_PROFILE = os.getenv('OCI_CONFIG_PROFILE', 'DEFAULT') ####################
#################### OCI_COMPARTMENT_ID = os.getenv('OCI_COMPARTMENT_ID', 'your_compartment_id_here') ####################
#################### OCI_MODEL_ID = os.getenv('OCI_MODEL_ID', 'your_model_id_here') ####################

import os

# OCI Configuration
OCI_CONFIG_PROFILE = os.getenv('OCI_CONFIG_PROFILE', 'DEFAULT')
OCI_COMPARTMENT_ID = os.getenv('OCI_COMPARTMENT_ID', 'ocid1.compartment.oc1..aaaaaaaaaf25ldyl5rxegseg4h4m2tpbvnecoh7w4tb5uisql2uhq32abrra')
OCI_MODEL_ID = os.getenv('OCI_MODEL_ID', 'ocid1.generativeaimodel.oc1.us-chicago-1.amaaaaaask7dceya7ozidbukxwtun4ocm4ngco2jukoaht5mygpgr6gq2lgq')

# Logging Configuration
LOG_FILE = os.getenv('LOG_FILE', 'business_categorizer.log')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Other Configuration
MAX_TOKENS = int(os.getenv('MAX_TOKENS', 4000))
TEMPERATURE = float(os.getenv('TEMPERATURE', 0))
FREQUENCY_PENALTY = float(os.getenv('FREQUENCY_PENALTY', 0))
TOP_P = float(os.getenv('TOP_P', 0))
TOP_K = int(os.getenv('TOP_K', 0))
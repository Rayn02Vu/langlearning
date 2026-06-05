#!/bin/bash
# Load environment variables from config/.env
set -a
source config/.env
set +a

# Run the Streamlit app
streamlit run src/main.py --server.runOnSave true
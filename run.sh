#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Run the app
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
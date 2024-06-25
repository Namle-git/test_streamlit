#!/bin/bash

# Start Flask app
gunicorn -b 0.0.0.0:5000 backend:app &

streamlit run app_deepspeech.py --server.port $PORT 

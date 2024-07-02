import streamlit as st
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from threading import Thread
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Flask app setup
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

@app.route('/string_upload', methods=['POST'])
def string_upload_handler():
    try:
        data = request.json
        logger.debug(f"Received string: {data['text']}")
        return jsonify({"message": "String received successfully"}), 200
    except Exception as e:
        logger.error(f"Error uploading string: {e}")
        return jsonify({"message": "Error uploading string", "error": str(e)}), 500

def run_flask():
    try:
        logger.info("Starting Flask server on port 5000")
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logger.error(f"Error starting Flask server: {e}")

def run_streamlit():
    try:
        logger.info("Starting Streamlit app")
        os.system('streamlit run app.py --server.port 8501')
    except Exception as e:
        logger.error(f"Error starting Streamlit app: {e}")

if __name__ == '__main__':
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    streamlit_thread = Thread(target=run_streamlit)
    streamlit_thread.start()
    flask_thread.join()
    streamlit_thread.join()

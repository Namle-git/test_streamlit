import streamlit as st
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from threading import Thread
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Flask app setup
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

@app.route('/string_upload', methods=['POST'])
def string_upload_handler():
    try:
        data = request.json
        logging.debug(f"Received string: {data['text']}")
        return jsonify({"message": "String received successfully"}), 200
    except Exception as e:
        logging.error(f"Error uploading string: {e}")
        return jsonify({"message": "Error uploading string", "error": str(e)}), 500

def run_flask():
    from waitress import serve
    logging.info("Starting Flask server with waitress on port 8000")
    serve(app, host='0.0.0.0', port=os.environ.get('PORT'))

def run_streamlit():
    logging.info("Starting Streamlit app")
    os.system('streamlit run app.py --server.port $PORT')

if __name__ == '__main__':
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    streamlit_thread = Thread(target=run_streamlit)
    streamlit_thread.start()
    flask_thread.join()
    streamlit_thread.join()

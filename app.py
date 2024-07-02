import streamlit as st
from threading import Thread
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Initialize Streamlit app
st.title("Basic String Communication Web App")

# HTML and JavaScript for sending a string
html_code = """
<script>
function sendString() {
    fetch('/string_upload', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: "Hello from the frontend!" })
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    }).then(data => {
        console.log("Received response:", data);
        document.getElementById("response").innerText = "Response: " + data.message;
    }).catch(error => {
        console.error("Error uploading string:", error);
        document.getElementById("response").innerText = "Error: " + error.message;
    });
}
</script>

<button onclick="sendString()">Send String</button>
<p id="response">Response: </p>
"""

# Include the HTML and JavaScript in the Streamlit app
st.components.v1.html(html_code, height=200)

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

# Function to run Flask server
def run_flask():
    app.run(host='0.0.0.0', port=8501, debug=True)

# Start Flask server in a separate thread
flask_thread = Thread(target=run_flask)
flask_thread.start()

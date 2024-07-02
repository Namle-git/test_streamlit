import streamlit as st
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Initialize Streamlit and Flask app
st.title("Basic String Communication Web App")
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# --- Flask Routes ---
@app.route('/string_upload', methods=['POST'])
def string_upload_handler():
    try:
        data = request.json
        logging.debug(f"Received string: {data['text']}")
        return jsonify({"message": "String received successfully"}), 200
    except Exception as e:
        logging.error(f"Error uploading string: {e}")
        return jsonify({"message": "Error uploading string", "error": str(e)}), 500

# --- Streamlit Frontend ---
html_code = f"""
<script>
function sendString() {{
    fetch('/string_upload', {{
        method: 'POST',
        headers: {{
            'Content-Type': 'application/json'
        }},
        body: JSON.stringify({{ text: "Hello from the frontend!" }})
    }}).then(response => {{
        if (!response.ok) {{
            throw new Error('Network response was not ok: ' + response.statusText);
        }}
        return response.json();
    }}).then(data => {{
        console.log("Received response:", data);
        document.getElementById("response").innerText = "Response: " + data.message;
    }}).catch(error => {{
        console.error("Error uploading string:", error);
        document.getElementById("response").innerText = "Error: " + error.message;
    }});
}}
</script>

<button onclick="sendString()">Send String</button>
<p id="response">Response: </p>
"""
st.components.v1.html(html_code, height=200)

# --- Run the app ---
if __name__ == "__main__":
    # For local development, comment out the line below and uncomment `app.run(...)`
    st.set_option('server.port', 8000)  # Set Streamlit to use the same port as Flask
    app.run(debug=True, host='0.0.0.0', port=8000) 
    #app.run(host='0.0.0.0', port=8501, debug=True)

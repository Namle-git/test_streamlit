from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

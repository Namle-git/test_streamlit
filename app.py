import streamlit as st

# Initialize Streamlit app
st.title("Basic String Communication Web App")

# HTML and JavaScript for sending a string
html_code = """
<script>
function sendString() {
    const url = `https://simonaireceptionistchatbot.azurewebsites.net:5000/string_upload`;
    fetch(url, {
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

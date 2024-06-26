import streamlit as st
from streamlit_mic_recorder import speech_to_text
import streamlit.components.v1 as components

st.title("AI Assistant with Automatic Speech Recognition")

# Function to automatically record and transcribe audio
def automatic_recording_and_transcription(duration: int = 5):
    text = speech_to_text(
        language='en',
        start_prompt="Record",
        stop_prompt="Stop",
        just_once=True,
        use_container_width=True,
        callback=None,
        args=(),
        kwargs={},
        key="mic_recorder"
    )
    return text

# Start automatic recording and transcription
transcription = automatic_recording_and_transcription(duration=5)

# HTML and JavaScript code
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simulate Button Click in Iframe</title>
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            function tryClickButton(attempts) {
                var iframe = document.getElementById('targetIframe');
                if (iframe && iframe.contentDocument) {
                    try {
                        var iframeDocument = iframe.contentDocument || iframe.contentWindow.document;
                        var button = iframeDocument.querySelector('.myButton');

                        if (button) {
                            button.click();
                            console.log('Button inside iframe clicked');
                        } else if (attempts > 0) {
                            console.log('Button not found, retrying...');
                            setTimeout(function() {
                                tryClickButton(attempts - 1);
                            }, 1000); // Retry after 1 second
                        } else {
                            console.log('Failed to click the button after 3 attempts');
                        }
                    } catch (e) {
                        console.log('Error accessing iframe content:', e);
                    }
                } else if (attempts > 0) {
                    console.log('Iframe not loaded yet, retrying...');
                    setTimeout(function() {
                        tryClickButton(attempts - 1);
                    }, 1000); // Retry after 1 second
                } else {
                    console.log('Iframe not loaded after 3 attempts');
                }
            }

            // Wait for the iframe to load and then start trying to click the button
            var iframe = document.getElementById('targetIframe');
            iframe.onload = function() {
                tryClickButton(3);
            };
        });
    </script>
</head>
<body>
    <iframe id="targetIframe" allow="accelerometer; ambient-light-sensor; autoplay; battery; camera; clipboard-write; document-domain; encrypted-media; fullscreen; geolocation; gyroscope; layout-animations; legacy-image-formats; magnetometer; microphone; midi; oversized-images; payment; picture-in-picture; publickey-credentials-get; sync-xhr; usb; vr ; wake-lock; xr-spatial-tracking" height="0" sandbox="allow-forms allow-modals allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts allow-downloads" scrolling="no" src="https://simonaireceptionistchatbot.azurewebsites.net/component/streamlit_mic_recorder.streamlit_mic_recorder/index.html?streamlitUrl=https%3A%2F%2Fsimonaireceptionistchatbot.azurewebsites.net%2F" style="display: none;" title="streamlit_mic_recorder.streamlit_mic_recorder" width="0"></iframe>
</body>
</html>
"""

# Embed the HTML and JavaScript in the Streamlit app
components.html(html_code, height=0, width=0)

# Display the transcription
if transcription:
    st.write(f"Transcription: {transcription}")
else:
    st.write("No transcription available.")

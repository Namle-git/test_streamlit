import streamlit as st
from streamlit_mic_recorder import speech_to_text
import streamlit.components.v1 as components

st.title("AI Assistant with Automatic Speech Recognition")

# Function to automatically record and transcribe audio

transcription = speech_to_text(
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


# JavaScript to interact with the button inside the iframe
# JavaScript to interact with the button inside the iframe
st.markdown("""
<script>
document.addEventListener("DOMContentLoaded", function() {
    function tryClickButton(attempts) {
        console.log("Attempting to find the iframe...");
        var iframe = document.querySelector('iframe[title="streamlit_mic_recorder.streamlit_mic_recorder"]');
        if (iframe) {
            console.log("Iframe found:", iframe);
            if (iframe.contentWindow) {
                try {
                    var iframeDocument = iframe.contentWindow.document;
                    console.log("Attempting to find the button in iframe...");
                    var button = iframeDocument.querySelector('.myButton');

                    if (button) {
                        console.log("Button found:", button);
                        button.click();
                        console.log('Button inside iframe clicked');
                    } else if (attempts > 0) {
                        console.log('Button not found, retrying...', attempts, 'attempts left');
                        setTimeout(function() {
                            tryClickButton(attempts - 1);
                        }, 1000); // Retry after 1 second
                    } else {
                        console.log('Failed to click the button after multiple attempts');
                    }
                } catch (e) {
                    console.log('Error accessing iframe content:', e);
                }
            } else {
                console.log("Iframe contentWindow not accessible.");
            }
        } else if (attempts > 0) {
            console.log('Iframe not found, retrying...', attempts, 'attempts left');
            setTimeout(function() {
                tryClickButton(attempts - 1);
            }, 1000); // Retry after 1 second
        } else {
            console.log('Iframe not loaded after multiple attempts');
        }
    }

    // Initial attempt to find and click the button
    tryClickButton(3);

        }
    });
});
</script>
""", unsafe_allow_html=True)

# Display the transcription
if transcription:
    st.write(f"Transcription: {transcription}")
else:
    st.write("No transcription available.")

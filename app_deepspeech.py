import streamlit as st
from streamlit_mic_recorder import mic_recorder
import streamlit.components.v1 as components

st.title("AI Assistant with Automatic Speech Recognition")

if st.button("Hello"):
    st.write("Button clicked")

# JavaScript to auto-click the button
js_code = """
<script>
document.addEventListener('DOMContentLoaded', (event) => {
  // Find the button using its attributes
  var button = document.querySelector('button[data-testid="baseButton-secondary"]');
  if (button) {
    button.click();
  }
});
</script>
"""

# Inject the JavaScript into the Streamlit app
components.html(js_code)


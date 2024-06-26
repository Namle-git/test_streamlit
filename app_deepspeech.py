import streamlit as st
import streamlit.components.v1 as components

st.title("AI Assistant with Automatic Speech Recognition")

button_clicked = st.button("Hello")

if button_clicked:
    st.write("Button clicked")

# JavaScript to auto-click the button
js_code = """
<script>
document.addEventListener('DOMContentLoaded', (event) => {
  // Find the button using its text content
  var buttons = document.getElementsByTagName('button');
  for (var i = 0; i < buttons.length; i++) {
    if (buttons[i].innerText === 'Hello') {
      buttons[i].click();
      break;
    }
  }
});
</script>
"""

# Inject the JavaScript into the Streamlit app
components.html(js_code)

import streamlit as st

# Initialize session state for button click
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

# Define the callback function to update the session state
def on_button_click():
    st.session_state.button_clicked = True

# Create a button with a callback function
st.button("Click Me!", on_click=on_button_click, key="click_button")

# Check the session state and display the confirmation message
if st.session_state.button_clicked:
    st.write("The button was clicked!")

# JavaScript to simulate the button click
simulate_click = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    const button = document.querySelector("button[aria-label='Click Me!']");
    if (button) {
        button.click();
    }
});
</script>
"""

# Inject the JavaScript into the app
st.markdown(simulate_click, unsafe_allow_html=True)

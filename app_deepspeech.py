import streamlit as st

# Function to display confirmation text
def button_clicked():
    st.write("The button was clicked!")

# Create a hidden Streamlit button
if st.button("Hidden Button", key="hidden_button"):
    button_clicked()

# HTML and JavaScript to simulate button click
html_code = """
<script>
function simulateClick() {
    document.getElementById("hiddenButton").click();
}
window.onload = simulateClick;
</script>
<button id="hiddenButton" style="display:none;"></button>
"""

# Display the HTML and JavaScript
st.markdown(html_code, unsafe_allow_html=True)

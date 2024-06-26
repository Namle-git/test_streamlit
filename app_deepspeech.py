import streamlit as st

# Function to simulate button click
def simulate_button_click():
    js_code = """
    <script>
    function simulateClick() {
        document.getElementById('clickButton').click();
    }
    simulateClick();
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)

# Function to display confirmation text
def button_clicked():
    st.write("The button was clicked!")

# Display the button
if st.button("Click Me!", key="clickButton"):
    button_clicked()

# Include JavaScript to simulate button click
simulate_button_click()

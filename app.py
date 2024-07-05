import streamlit as st
import streamlit.components.v1 as components

html_code = """
<script>
    fetch('https://yourappname.azurewebsites.net/flask/test', {
        method: 'GET'
    }).then(response => response.json())
    .then(data => {
        alert(data.message);
    }).catch(error => {
        console.error('Error:', error);
    });
</script>
"""

components.html(html_code, height=600)

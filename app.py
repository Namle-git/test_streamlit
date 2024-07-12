import os
import streamlit as st
import requests

st.title('Streamlit and Flask Communication')

# Use an environment variable or relative URL
api_url = os.environ.get('FLASK_API_URL', '/flask/api/data')
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    st.write(data['message'])
else:
    st.write('Failed to get data from Flask')

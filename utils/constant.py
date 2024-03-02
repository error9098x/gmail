import os
# from dotenv import load_dotenv
# from os.path import join, dirname, abspath

# # Construct the path to the .env file
# dotenv_path = join(dirname(dirname(abspath(__file__))), '.env')

# # Load the .env file
# load_dotenv(dotenv_path)

# # Retrieve environment variables
# SMTP_SERVER_ADDRESS = os.getenv('SMTP_SERVER_ADDRESS')
# PORT = os.getenv('PORT')
# SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
# SENDER_ADDRESS = os.getenv('SENDER_ADDRESS')

import streamlit as st

SMTP_SERVER_ADDRESS = st.secrets['SMTP_SERVER_ADDRESS']
PORT = st.secrets['PORT']
SENDER_PASSWORD = st.secrets['SENDER_PASSWORD']
SENDER_ADDRESS = st.secrets['SENDER_ADDRESS']
st.write(SMTP_SERVER_ADDRESS)
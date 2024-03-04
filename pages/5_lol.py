import streamlit as st
from utils.helper import send_email
from utils.constant import (SMTP_SERVER_ADDRESS, PORT, SENDER_PASSWORD, SENDER_ADDRESS)


def main():
    with st.form("Email Form"):
        # Define a list of pre-defined subjects
        subjects = ["Fraud Complaint", "Corruption Complaint", "Customer Service Issue", "Product Defect", "Illegal Activity Report"]

        # Use selectbox to show the dropdown and select a subject
        subject = st.selectbox("Select document", options=subjects)

        fullName = st.text_input(label='Full Name', placeholder="Please enter your full name")
        email = st.text_input(label='Email Address', placeholder="Please enter email address of the government entity")
        youremail = st.text_input(label='Email Address', placeholder="Please enter your email address")
        text = st.text_area(label='Email Text', placeholder="Please enter your text here")
        uploaded_file = st.file_uploader("Attachment")
        submit_res = st.form_submit_button(label='Send')

    if submit_res:
        if not (subject and fullName and email and text and uploaded_file):
            st.error('All fields must be filled before sending.')
        else:
            extra_info = """
    ----------------------------------------
    Email Address of User: {}
    User Full Name: {}
    ----------------------------------------
    """.format(youremail, fullName)

            message = extra_info + text

            send_email(sender=SENDER_ADDRESS, password=SENDER_PASSWORD,
                    receiver=email, smtp_server=SMTP_SERVER_ADDRESS, smtp_port=PORT,
                    email_message=message, subject=subject, attachment=uploaded_file,cc=youremail)

if __name__ == '__main__':
    st.write("This is the base structure of the app which will be completed")
    main()
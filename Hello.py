import streamlit as st
from utils.helper import send_email
#from utils.constant import (SMTP_SERVER_ADDRESS, PORT, SENDER_PASSWORD, SENDER_ADDRESS)


def main():
    with st.form("Email Form"):
        subject = st.text_input(label='Subject', placeholder="Please enter subject of your mail")
        fullName = st.text_input(label='Full Name', placeholder="Please enter your full name")
        email = st.text_input(label='Email Address', placeholder="Please enter your email address")
        text = st.text_area(label='Email Text', placeholder="Please enter your text here")
        uploaded_file = st.file_uploader("Attachment")
        submit_res = st.form_submit_button(label='Send')

    if submit_res:
        extra_info = """
----------------------------------------
Email Address of Sender: {}
Sender Full Name: {}
----------------------------------------
""".format(email, fullName)

        message = extra_info + text

        send_email(sender=SENDER_ADDRESS, password=SENDER_PASSWORD,
                   receiver=email, smtp_server=SMTP_SERVER_ADDRESS, smtp_port=PORT,
                   email_message=message, subject=subject, attachment=uploaded_file)

if __name__ == '__main__':
    st.write("This is the base structure of the app which will be completed")
    main()
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE

def send_email(sender, password, receiver, smtp_server, smtp_port, email_message, subject, attachment=None, is_html=False):
    # Create a MIMEMultipart object to combine the different parts of the email
    message = MIMEMultipart()
    message['To'] = COMMASPACE.join([receiver])  # Allow for a list of receivers
    message['From'] = sender
    message['Subject'] = subject

    # Attach the email body
    if is_html:
        # For HTML messages
        message.attach(MIMEText(email_message, 'html', 'utf-8'))
    else:
        # For plain text messages
        message.attach(MIMEText(email_message, 'plain', 'utf-8'))

    # Check if there is an attachment provided
    if attachment:
        # Guess the MIME type based on the name of the attachment
        maintype, _, subtype = (attachment.type or 'application/octet-stream').partition('/')
        # Create a MIMEApplication object for the attachment
        att = MIMEApplication(attachment.read(), _subtype=subtype)
        att.add_header('Content-Disposition', 'attachment', filename=attachment.name)
        message.attach(att)  # Attach the attachment to the message

    # Establish a connection to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Start TLS encryption for the connection
    server.login(sender, password)  # Log in to the server using the provided credentials
    text = message.as_string()  # Convert the message to a string
    server.sendmail(sender, receiver, text)  # Send the email
    server.quit()  # Terminate the server connection

# Now you can call send_email function with the is_html parameter set to True if you are sending an HTML email.
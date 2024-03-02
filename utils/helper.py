# Import required modules
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication

# Define the function to send emails
def send_email(sender, password, receiver, smtp_server, smtp_port, email_message, subject, attachment=None):
    # Create a MIMEMultipart object to combine the different parts of the email
    message = MIMEMultipart()
    message['To'] = Header(receiver)   # Set the receiver's email address
    message['From'] = Header(sender)  # Set the sender's email address
    message['Subject'] = Header(subject)  # Set the email's subject

    # Attach the email body with utf-8 encoding
    message.attach(MIMEText(email_message, 'plain', 'utf-8'))

    # Check if there is an attachment provided
    if attachment:
        # Create a MIMEApplication object for the attachment with the text subtype
        att = MIMEApplication(attachment.read(), _subtype="txt")
        att.add_header('Content-Disposition', 'attachment', filename=attachment.name)
        message.attach(att)  # Attach the attachment to the message

    # Establish a connection to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Start TLS encryption for the connection
    server.login(sender, password)  # Log in to the server using the provided credentials
    text = message.as_string()  # Convert the message to a string
    server.sendmail(sender, receiver, text)  # Send the email
    server.quit()  # Terminate the server connection

# At this point, you can call the send_email function with the appropriate arguments
# to send an email. The arguments would be the sender's email, password, receiver's email,
# the SMTP server address, SMTP server port, email body message, subject line,
# and an optional attachment file.
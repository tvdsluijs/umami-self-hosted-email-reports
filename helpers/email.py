"""
📧 Email Sending Helper

This module provides a function to send emails using an SMTP server. It supports
customizable subject lines, email content, and recipient lists.

Functions:
- send_email: Sends an email with the given content to specified recipients.
"""

import smtplib
from email.mime.multipart import MIMEMultipart

def send_email(subject, email_content, recipient_emails, smtp_config):
    """
    Sends an email using the provided SMTP configuration.

    Args:
        subject (str): Subject of the email.
        email_content (MIMEText): The email body as a MIMEText object.
        recipient_emails (list): List of recipient email addresses.
        smtp_config (dict): SMTP configuration details, including:
            - host (str): SMTP server host.
            - port (int): SMTP server port.
            - username (str): SMTP username.
            - password (str): SMTP password.
            - from_email (str): Sender's email address.

    Raises:
        Exception: If sending the email fails.
    """
    try:
        # Create the email container (MIMEMultipart object)
        msg = MIMEMultipart()
        msg['From'] = smtp_config['from_email']  # Set sender's email address
        msg['To'] = ", ".join(recipient_emails)  # Join recipient emails into a string
        msg['Subject'] = subject  # Set the email subject

        # Attach the email content (body)
        msg.attach(email_content)

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_config['host'], smtp_config['port']) as server:
            server.starttls()  # Enable TLS encryption
            server.login(smtp_config['username'], smtp_config['password'])  # Login with credentials
            server.sendmail(
                smtp_config['from_email'], recipient_emails, msg.as_string()
            )  # Send the email

    except Exception as e:
        # Handle any exceptions during the email sending process
        print(f"Failed to send email: {e}")

"""
📧 Email Sending Helper

This module provides a function to send emails using an SMTP server. It supports
customizable subject lines, email content, and recipient lists.

Functions:
- send_email: Sends an email with the given content to specified recipients.
"""
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

logger = logging.getLogger(__name__)

def send_email(subject, email_content, recipient_emails, smtp_config, pdf_filename):
    """
    Sends an email using the provided SMTP configuration.

    Args:
        subject (str): Subject of the email.
        email_content (MIMEText): The email body as a MIMEText object.
        recipient_emails (list): List of recipient email addresses.
        pdf-filename (str): The filename of the PDF to attach to the email.
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
        msg.attach(MIMEText(email_content, 'html'))

        # Attach the PDF file if provided
        if pdf_filename:
            try:
                with open(pdf_filename, 'rb') as pdf_file:
                    pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")
                    pdf_attachment.add_header('Content-Disposition', 'attachment', filename=pdf_filename)
                    msg.attach(pdf_attachment)
            except Exception as e:
                logger.error(f"Failed to attach PDF: {e}")

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_config['host'], smtp_config['port']) as server:
            server.starttls()  # Enable TLS encryption
            server.login(smtp_config['username'], smtp_config['password'])  # Login with credentials
            server.sendmail(
                smtp_config['from_email'], recipient_emails, msg.as_string()
            )  # Send the email

    except Exception as e:
        # Handle any exceptions during the email sending process
        logger.error(f"Failed to send email: {e}")

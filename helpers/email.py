import smtplib
from email.mime.multipart import MIMEMultipart

def send_email(subject, email_content, recipient_emails, smtp_config):
    """
    Sends an email using the provided SMTP configuration.
    :param subject: Subject of the email.
    :param email_content: MIMEText object containing the email body.
    :param sender_email: Email address of the sender.
    :param recipient_emails: List of recipient email addresses.
    :param smtp_config: Dictionary with SMTP server details (host, port, username, password).
    """
    try:
        # Create the email container
        msg = MIMEMultipart()
        msg['From'] = smtp_config['from_email']
        msg['To'] = ", ".join(recipient_emails)
        msg['Subject'] = subject

        # Attach the email content
        msg.attach(email_content)

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_config['host'], smtp_config['port']) as server:
            server.starttls()  # Enable encryption
            server.login(smtp_config['username'], smtp_config['password'])
            server.sendmail(smtp_config['from_email'], recipient_emails, msg.as_string())

    except Exception as e:
        print(f"Failed to send email: {e}")

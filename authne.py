import smtplib
from email.mime.text import MIMEText

def send_email(to_email, subject, message):
    # Set your email and password or API key
    email_address = "sainirahul1009@gmail.com"
    email_password = "User@123"

    # Set up the message
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = to_email

    # Connect to the SMTP server and send the email
    with smtplib.SMTP("smtp.your-email-provider.com", 587) as server:
        server.starttls()
        server.login(email_address, email_password)
        server.sendmail(email_address, to_email, msg.as_string())

# Example usage
to_email = "dhruvs408@gmail.com"
subject = "Price Alert Notification"
message = "The price has reached your target. You have a new alert!"
send_email(to_email, subject, message)

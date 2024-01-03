import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email():
    # Email configuration
    # sender_email = 'your_email@gmail.com'
    # receiver_email = 'ntnzelenin@gmail.com'
    # subject = 'Testing sending email from python'
    # body = 'Body of the email'
    #
    # # Email server configuration (for Gmail)
    # smtp_server = 'smtp.gmail.com'
    # smtp_port = 587
    # smtp_username = 'your_email@gmail.com'
    # smtp_password = 'your_email_password'
    #
    # message = MIMEMultipart()
    # message['From'] = sender_email
    # message['To'] = receiver_email
    # message['Subject'] = subject
    #
    # message.attach(MIMEText(body, 'plain'))
    #
    # with smtplib.SMTP(smtp_server, smtp_port) as server:
    #     server.starttls()
    #     server.login(smtp_username, smtp_password)
    #
    #     server.sendmail(sender_email, receiver_email, message.as_string())
    #
    # print("Email sent successfully!")
    pass

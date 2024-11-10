import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_jwt_extended import create_access_token
from dotenv import load_dotenv
import os

load_dotenv()

def send_email(email, body, subject):
    msg = MIMEMultipart()
    msg['From'] = os.getenv('EMAIL_USER')
    msg['To'] = email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    print(os.getenv('SMTP_SERVER'), os.getenv('SMTP_PORT'), os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
    with smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT'))) as server:
        server.ehlo()
        server.starttls()
        server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
        server.send_message(msg)
        print("отправил")
        return "отправил"
    return "не отправил"

def send_activation_email(email, token):
    '''
    Отправляет письмо с активацией аккаунта.

    :param email: Электронная почта получателя.
    :param token: Токен активации.
    :return: None
    '''
    local_ip = os.getenv('LOCAL_IP')
    local_port = os.getenv('LOCAL_PORT')
    link = f'http://{local_ip}:{local_port}/activate?key={token}&email={email}'
    body = f'<a href="{link}">Click here to activate your account</a>'
    send_email(email, body, 'Account activation')
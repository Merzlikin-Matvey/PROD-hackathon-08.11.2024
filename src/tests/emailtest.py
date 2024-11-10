import unittest
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


class TestEmail(unittest.TestCase):
    def test_sending(self):
        self.assertEqual("отправил",send_email("levkerskij@gmail.com",subject="1234",body="<h1>1</h1>"))
        self.assertEqual("отправил",send_email("levkerskij@gmail.com",subject="aaaaa",body="<h1>2</h1>"))
        self.assertEqual("отправил",send_email("levkerskij@gmail.com",subject="test",body="<h1>3</h1>"))



if __name__ == "__main__":
    unittest.main()
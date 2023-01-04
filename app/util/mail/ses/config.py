import os
from dotenv import load_dotenv


load_dotenv()

class SESMailer:
    def __init__(self, 
                 SENDER=os.getenv('SES_SENDER'), 
                 SENDER_NAME=os.getenv('SES_SENDER_NAME'), 
                 USERNAME_SMTP=os.getenv('SES_USERNAME_SMTP'), 
                 PASSWORD_SMTP=os.getenv('SES_PASSWORD_SMTP'), 
                 HOST=os.getenv('SES_HOST'),
                 PORT=465):
        self.SENDER=SENDER
        self.SENDER_NAME=SENDER_NAME
        self.USERNAME_SMTP=USERNAME_SMTP
        self.PASSWORD_SMTP=PASSWORD_SMTP
        self.HOST=HOST
        self.PORT=PORT
        


from app.util.mail.config import Message as Mail
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

def send_mail(RECIPIENT, TOKEN, TYPE, **kwargs):
    mailer = Mail(RECIPIENT, TOKEN, TYPE, **kwargs)
    try:  
        with smtplib.SMTP_SSL(mailer.HOST, mailer.PORT) as server:
            server.login(mailer.USERNAME_SMTP, mailer.PASSWORD_SMTP)
            server.sendmail(mailer.SENDER, RECIPIENT, mailer.msg.as_string())
            server.close()
    except Exception as e:
        print ("Error: ", e)

def send_application_mail(RECIPIENT, TOKEN, user_name, job_title):
    try:
        send_mail(os.getenv('HIRING_EMAIL'), TOKEN, TYPE="application_notification", user_name=user_name, job_title=job_title)
        send_mail(RECIPIENT, TOKEN, TYPE="application_confirmation")

    except Exception as e:
        print('Error: ', e)

def send_accept_mail(RECIPIENT, TOKEN, user_name, job_title, accept_subject, accept_body):
    try:
        send_mail(RECIPIENT, TOKEN, TYPE="accept_notification", user_name=user_name, job_title=job_title, accept_subject=accept_subject, accept_body=accept_body)
    except Exception as e:
        print('Error: ', e)

def send_reject_mail(RECIPIENT, TOKEN, user_name, job_title, reject_subject, reject_body):
    try:
        send_mail(RECIPIENT, TOKEN, TYPE="reject_notification", user_name=user_name, job_title=job_title, reject_subject=reject_subject, reject_body=reject_body)
    except Exception as e:
        print('Error: ', e)
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.util.mail.ses import SES as Mailer
import os
from dotenv import load_dotenv


load_dotenv()
    
        
class Message(Mailer):        
    def __init__(self, RECIPIENT, TOKEN, TYPE, user_name=None, job_title=None, accept_subject=None, accept_body=None, URL=os.getenv('URL')):
        Mailer.__init__(self)
        self.RECIPIENT=RECIPIENT
        self.TOKEN=TOKEN
        self.URL=URL
        self.user_name = user_name
        self.job_title = job_title
        self.accept_subject = accept_subject
        self.accept_body = accept_body
        
        if TYPE == "user_validation":
            # The email body for recipients with non-HTML email clients.
            self.SUBJECT="Validation Email"
            BODY_TEXT = ("Validation Email\r\n"
                        "This email is an automated message."
                        "Verify your account at %s/profile/validate/%s" % (self.URL, self.TOKEN)
                        )
            
            # The HTML body of the email.
            BODY_HTML = f"""<html>
            <head></head>
            <body>
            <h1>Validation Email</h1>
            <p>This email is an automated message. Please validate your email.
                <a href='https://{self.URL}/profile/validate/{self.TOKEN}'>Account Validation</a>
            </p>
            </body>
            </html>
            """
        elif TYPE == "password_reset":
            self.SUBJECT="Password Reset Email"
            BODY_TEXT = ("Password Reset Email\r\n"
                        "This email is an automated message."
                        "Reset your password within the next 60 minutes at %s/reset-password/%s" % (self.URL, self.TOKEN)
                        )

            # The HTML body of the email.
            BODY_HTML = f"""<html>
            <head></head>
            <body>
            <h1>Password Reset Email</h1>
            <p>This email is an automated message. Please reset your password within the next 60 minutes.
                <a href='https://{self.URL}/reset-password/{self.TOKEN}'>Reset password</a>
            </p>
            </body>
            </html>
            """
        elif TYPE == "application_confirmation":
            self.SUBJECT="Application Confirmation"
            BODY_TEXT = ("Thank you for your application\r\n"
                        "This email is an automated message."
                        "We will be in touch soon."
                        )
            BODY_HTML = f"""<html>
            <head></head>
            <body>
            <h1>Application Confirmation</h1>
            <p>This email is an automated message. We will be in touch soon.</p>
            </body>
            </html>
            """
        elif TYPE == "application_notification":
            self.SUBJECT="New Application"
            BODY_TEXT = ("New Application Recieved\r\n"
                         "User {self.user_name} applied for the position of {self.job_title}.") 
            BODY_HTML = f"""<html>
                <head></head>
                <body>
                <h1>New Application Recieved</h1>
                <p>User {self.user_name} applied for the position of {self.job_title}.</p>
                </body>
                </html>
            """
        elif TYPE == "accept_notification":
            self.SUBJECT = self.accept_subject
            BODY_TEXT = self.accept_body
            BODY_HTML = f"""<html>
                <head></head>
                <body>
                <h1>Thank you for your application!</h1>
                <p>{ self.accept_body }</p>
                </body>
                </html>
            """
        elif TYPE == "reject_notification":
            self.SUBJECT="Thank you for your application"
            BODY_TEXT = ("Thank you for your application for the position of {self.job_title}. We have reviewed your application and have decided not to move forward at this time. We appreciate your interest and wish you the best of luck in your job search.") 
            BODY_HTML = f"""<html>
                <head></head>
                <body>
                <h1>Thank you for your application</h1>
                <p>Thank you for your application for the position of {self.job_title}. We have reviewed your application and have decided not to move forward at this time. We appreciate your interest and wish you the best of luck in your job search.</p>
                </body>
                </html>
            """

        # Create message container - the correct MIME type is multipart/alternative.
        self.msg = MIMEMultipart('alternative')
        self.msg['Subject'] = self.SUBJECT
        

        if TYPE == "application_confirmation" or TYPE == "application_notification" or TYPE == 'reject_notification':
            self.msg['From'] = email.utils.formataddr(('Tobu Pengin', 'no-reply@tobupengin.com'))

        elif TYPE == 'accept_notification':
            self.msg['From'] = email.utils.formataddr(('Tobu Pengin', os.getenv('HIRING_EMAIL')))

        else:
            self.msg['From'] = email.utils.formataddr((self.SENDER_NAME, self.SENDER))

        self.msg['To'] = RECIPIENT

        # Record the MIME types of both parts - text/plain and text/html.
        self.part1 = MIMEText(BODY_TEXT, 'plain')
        self.part2 = MIMEText(BODY_HTML, 'html')
        
        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        self.msg.attach(self.part1)
        self.msg.attach(self.part2)
        
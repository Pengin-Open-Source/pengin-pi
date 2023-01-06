import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.util.mail.ses import SES as Mailer
import os
from dotenv import load_dotenv


load_dotenv()
    
        
class Message(Mailer):        
    def __init__(self, RECIPIENT, TOKEN, URL=os.getenv('URL')):
        Mailer.__init__(self)
        self.RECIPIENT=RECIPIENT
        self.TOKEN=TOKEN
        self.URL=URL
        self.SUBJECT="Validation Email"
        # The email body for recipients with non-HTML email clients.
        BODY_TEXT = ("Validation Email\r\n"
                    "This email is an automated message."
                    "Verify your accout at %s/validate/%s" % (self.URL, self.TOKEN)
                    )
        
        # The HTML body of the email.
        BODY_HTML = f"""<html>
        <head></head>
        <body>
        <h1>Validation Email</h1>
        <p>This email is an automated message.  Please validate your email.
            <a href='https://{self.URL}/profile/validate/{self.TOKEN}'>Account Validation</a>
        </p>
        </body>
        </html>
        """
        
        # Create message container - the correct MIME type is multipart/alternative.
        self.msg = MIMEMultipart('alternative')
        self.msg['Subject'] = self.SUBJECT
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
        
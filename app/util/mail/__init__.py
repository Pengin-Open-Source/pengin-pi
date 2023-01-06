from app.util.mail.config import Message as Mail
import smtplib


def send_mail(RECIPIENT, TOKEN):
    mailer=Mail(RECIPIENT,TOKEN)
    try:  
        with smtplib.SMTP_SSL(mailer.HOST, mailer.PORT) as server:
            server.login(mailer.USERNAME_SMTP, mailer.PASSWORD_SMTP)
            server.sendmail(mailer.SENDER, RECIPIENT, mailer.msg.as_string())
            server.close()
    # Display an error message if something goes wrong.
    except Exception as e:
        print ("Error: ", e)
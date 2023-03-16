import smtplib
import ssl


class Email:
    def __init__(self, smtp_server, email_credentials):
        self.server = smtp_server.domain
        self.port = smtp_server.port
        self.user = email_credentials.login
        self.password = email_credentials.password

    def send(self, _from, _to, subject, text):
        message = "From: {}\nTo: {}\nSubject: {}\n\n{}".format(_from, _to, subject, text)
        context = ssl.create_default_context()
        with smtplib.SMTP(self.server, self.port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.login(self.user, self.password)
            server.sendmail(_from, _to, message)


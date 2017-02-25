import smtplib
from email.mime.text import MIMEText

import config


class AhabEmailSender:
    def __init__(self, email_type, to, body, subject=None):
        if subject is None:
            self.subject = email_type

        try:
            self.email_credentials = config.EMAIL_CREDENTIALS[email_type]
        except KeyError:
            raise KeyError("No credentials found for " + email_type)

        self.host_name = self.email_credentials['host_name']
        self.from_address = self.email_credentials['from']

        self.msg = MIMEText(body)
        self.msg['Subject'] = self.subject
        self.msg['From'] = self.from_address
        self.msg['To'] = to

    def send(self):
        self.s = smtplib.SMTP(self.host_name)
        self.s.send_message(self.msg)
        self.s.quit()

if __name__ == "__main__":
    email = dict()
    email['body'] = "test"
    email['to'] = "martinleewatts@gmail.com"
    email['subject'] = "subjectey"

    email_sender = AhabEmailSender("arbitrage", email)
    email_sender.send()

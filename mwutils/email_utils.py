import smtplib
from email.mime.text import MIMEText

import mwutils.config as config


class AhabEmailSender:
    def __init__(self, email_type, to, body, subject=None, sub_type='plain'):
        if subject is None:
            self.subject = email_type
        else:
            self.subject = subject

        try:
            self.email_credentials = config.EMAIL_CREDENTIALS[email_type]
        except KeyError:
            raise KeyError("No credentials found for " + email_type)

        self.host_name = self.email_credentials['host_name']
        self.from_address = self.email_credentials['from']

        self.msg = MIMEText(body, sub_type)
        self.msg['Subject'] = self.subject
        self.msg['From'] = self.from_address
        self.msg['To'] = to

    def send(self):
        self.s = smtplib.SMTP(self.host_name)
        self.s.send_message(self.msg)
        self.s.quit()

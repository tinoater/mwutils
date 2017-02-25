import unittest

import emailUtils


class EmailSendingTestCase(unittest.TestCase):
    """Tests for AhabEmailSender class, will send out emails to martinleewatts@gmail.com"""

    def test_basic_email(self):
        body = "unit test"
        to = "martinleewatts@gmail.com"
        subject = "Unit Test for email sending"

        email = emailUtils.AhabEmailSender("testing", to, body, subject)
        email.send()

    def test_basic_email_no_subject(self):
        body = "unit test"
        to = "martinleewatts@gmail.com"

        email = emailUtils.AhabEmailSender("testing", to, body)
        email.send()

    def test_email_incorrect_email_type(self):
        to = "dummy"
        body = "dummy"
        self.assertRaises(KeyError, lambda: emailUtils.AhabEmailSender("NotARealThing", to, body))

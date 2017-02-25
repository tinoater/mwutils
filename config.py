# CONFIG paths and variables go here
import os
from sys import platform


SELENIUM_IMPLICIT_WAIT = 30


if platform == "linux" or platform == "linux2":
    WEBDRIVER_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Files\\chromedriver")
elif platform == "win32":
    WEBDRIVER_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Files\\chromedriver_win.exe")

EMAIL_CREDENTIALS = dict()
EMAIL_CREDENTIALS['arbitrage'] = {'host_name': 'localhost',
                                  'from': 'arbitrage@ahabEmails'}
EMAIL_CREDENTIALS['testing'] = {'host_name': 'localhost',
                             'from': 'testing@ahabEmails'}

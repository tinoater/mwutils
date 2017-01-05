# CONFIG paths and variables go here
import os
from sys import platform

if platform == "linux" or platform == "linux2":
    WEBDRIVER_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Files\\chromedriver")
elif platform == "win32":
    WEBDRIVER_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Files\\chromedriver_win.exe")
import unittest
import os
from bs4 import BeautifulSoup
from sys import platform

from .context import utils
from .context import email_utils

if platform == "linux" or platform == "linux2":
    WEBDRIVER_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Files\\chromedriver")
elif platform == "win32":
    WEBDRIVER_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Files\\chromedriver_win.exe")

# --------------------------
# Constants class tests
# --------------------------
class ConstantsExceptionsTestCase(unittest.TestCase):
    """Tests for Constants class exceptions in mwutils.py."""

    def test_no_file(self):
        """Does it fail correctly when file not found?"""
        self.assertRaises(FileNotFoundError, lambda: utils.Constants('FileNotThere.const'))


class ConstantsStringTestCase(unittest.TestCase):
    """Tests for Constants class - string variables"""

    def test_simple_string(self):
        """Can it load a simple string variable?"""
        self.assertEqual(self.string_test.STRING, "Simple string")

    def test_comma_separated_string(self):
        """Can it load a comma separated string variable?"""
        self.assertEqual(self.string_test.STRING_COMMA, "Simple, string")

    def test_long_string(self):
        """Can it load a long string variable?"""
        self.assertEqual(self.string_test.STRING_LONG, "Simple1, Simple2, Simple3, Simple4, Simple5, Simple6, Simple7, "
                                                       "Simple8, Simple9, Simple10")

    def test_very_long_string(self):
        """Can it load a really long string variable?"""
        self.assertEqual(len(self.string_test.STRING_REALLY_LONG), 899)

    def test_newline_string(self):
        """Can it load a newline string variable?"""
        self.assertEqual(self.string_test.STRING_NEWLINE, "Simple\n string")

    def setUp(self):
        self.string_test = utils.Constants("string_basic.const")


class ConstantsNumberTestCase(unittest.TestCase):
    """Tests for Constants class - number variables"""

    def test_integer_number(self):
        """Can it load an integer variable?"""
        self.assertEqual(self.number_test.NUMBER_INTEGER, 1)

    def test_decimal_number(self):
        """Can it load a decimal variable?"""
        self.assertEqual(self.number_test.NUMBER_DECIMAL, 1.3)

    def test_long_decimal_number(self):
        """Can it load a long decimal variable?"""
        self.assertEqual(self.number_test.NUMBER_DECIMAL_LONG, 1.23456789)

    def test_negative_number(self):
        """Can it load a negative variable?"""
        self.assertEqual(self.number_test.NUMBER_NEGATIVE, -0.05)

    def setUp(self):
        self.number_test = utils.Constants("number_basic.const")


class ConstantsDictionaryTestCase(unittest.TestCase):
    """Tests for Constants class - dictionary variables"""

    def test_string_dictionary(self):
        """Can it load a single string dictionary?"""
        self.assertEqual(self.dictionary_test.DICT_ONE_STRING["key1"], "value1")
        self.assertEqual(len(self.dictionary_test.DICT_ONE_STRING), 1)

    def test_multiple_string_dictionary(self):
        """Can it load a multiple string dictionary?"""
        self.assertEqual(self.dictionary_test.DICT_TWO_STRING["key1"], "value1")
        self.assertEqual(self.dictionary_test.DICT_TWO_STRING["key2"], "value2")
        self.assertEqual(len(self.dictionary_test.DICT_TWO_STRING), 2)

    def test_multiline_string_dictionary(self):
        """Can it load a multiline string dictionary?"""
        self.assertEqual(self.dictionary_test.DICT_MULTILINE_STRING["key1"], "thing1")
        self.assertEqual(self.dictionary_test.DICT_MULTILINE_STRING["key2"], "thing2")
        self.assertEqual(self.dictionary_test.DICT_MULTILINE_STRING["key3"], "thing3")
        self.assertEqual(len(self.dictionary_test.DICT_MULTILINE_STRING), 3)

    def test_number_dictionary(self):
        """Can it load a number dictionary?"""
        self.assertEqual(self.dictionary_test.DICT_ONE_NUMBER["key1"], 10.5)
        self.assertEqual(len(self.dictionary_test.DICT_ONE_NUMBER), 1)

    def setUp(self):
        self.dictionary_test = utils.Constants("dictionary_basic.const")


class ConstantsBettingTestCase(unittest.TestCase):
    """Tests for Constants class - real betting variables"""

    def test_first_strings(self):
        """Can it load the first string variables?"""
        self.assertEqual(self.real_test.WEBDRIVER_PATH, "F:\Coding\PycharmProjects\Arbitrage\chromedriver.exe")
        self.assertEqual(self.real_test.ARBITRAGE_PATH, "F:\Coding\PycharmProjects\Arbitrage\ScrapedFiles")
        self.assertEqual(self.real_test.RESULTS_PATH, "F:\Coding\PycharmProjects\Arbitrage\Results")
        self.assertEqual(self.real_test.SUMMARY_RESULTS_PATH, "F:\Coding\PycharmProjects\Arbitrage\SummaryResults")

    def test_commented_dictionary(self):
        """Can it load a partially commented out dictionary?"""
        self.assertEqual(len(self.real_test.BOOKMAKERS_LIST), 3)
        self.assertEqual(self.real_test.BOOKMAKERS_LIST["EIGHT88"], 0)
        self.assertEqual(self.real_test.BOOKMAKERS_LIST["PADDYPOWER"], 1)
        self.assertEqual(self.real_test.BOOKMAKERS_LIST["WILLIAMHILL"], 3)

    def test_large_dictionary(self):
        """Can it load a big string dictionary?"""
        self.assertEqual(len(self.real_test.EIGHT88_DICT), 8)
        self.assertEqual(self.real_test.EIGHT88_DICT["Bookmaker"], "888")
        self.assertEqual(self.real_test.EIGHT88_DICT["Football_LaLig"], "https://www.888sport.com/bet/#/filter/football/spain/laliga")
        self.assertEqual(self.real_test.EIGHT88_DICT["Football_GeBun"], "https://www.888sport.com/bet/#/filter/football/germany/bundesliga")

    def test_very_large_dictionary(self):
        """Can it load a very long string dictionary?"""
        self.assertEqual(len(self.real_test.FOOTBALL_DICT), 263)

    def setUp(self):
        self.real_test = utils.Constants("real_file.const")


# --------------------------
# Page source URL function tests
# --------------------------
class GetPageSourceURLTestCase(unittest.TestCase):
    """Tests for the get_page_source_url function in utils.py."""

    def setUp(self):
        self.html_soup = utils.get_page_source_url("https://en.wikipedia.org/wiki/St_Columb_Major",
                                                     WEBDRIVER_PATH,
                                                     os.path.join(os.path.curdir, "output/st_columb_wiki.txt"),
                                                     sleep_time=2)

    def tearDown(self):
        try:
            os.remove(os.path.join(os.path.curdir, "output/st_columb_wiki.txt"))
        except OSError:
            pass

    def test_page_downloads(self):
        """Check that the page was downloaded to the out directory, is non empty and matches the html_soup"""
        self.assertTrue(os.path.exists(os.path.join(os.path.curdir, "output/st_columb_wiki.txt")))

        with open(os.path.join(os.path.curdir, "output/st_columb_wiki.txt")) as f:
            self.text = f.read()
            self.soup_from_text = BeautifulSoup(self.text, "lxml")

        self.assertTrue(len(self.text) > 1)
        self.assertEqual(self.soup_from_text, self.html_soup)

    def test_page_downloads_correctly(self):
        """Check that the file has the correct content"""
        self.assertEqual(len(self.html_soup.findAll("h2")), 13)


class GetPageSourceTestCase(unittest.TestCase):
    """Tests for the get_page_source function in utils.py."""

    def test_url_download(self):
        self.html_soup = utils.get_page_source(url="https://en.wikipedia.org/wiki/St_Columb_Major",
                                                 webdriver_path=WEBDRIVER_PATH,
                                                 file_path=os.path.join(os.path.curdir, "output/st_columb_wiki_perm.txt"),
                                                 sleep_time=2)

        self.assertTrue(os.path.exists(os.path.join(os.path.curdir, "output/st_columb_wiki_perm.txt")))
        self.assertEqual(len(self.html_soup.findAll("h2")), 13)

    def tearDown(self):
        try:
            os.remove(os.path.join(os.path.curdir, "output/st_columb_wiki_perm.txt"))
        except OSError:
            pass
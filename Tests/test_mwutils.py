import unittest

import mwutils


# --------------------------
# Constants class tests
# --------------------------
class ConstantsExceptionsTestCase(unittest.TestCase):
    """Tests for Constants class exceptions in mwutils.py."""

    def test_no_file(self):
        """Does it fail correctly when file not found?"""
        self.assertRaises(FileNotFoundError, lambda: mwutils.Constants('FileNotThere.const'))


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
        self.string_test = mwutils.Constants("string_basic.const")


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
        self.number_test = mwutils.Constants("number_basic.const")


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
        self.assertEqual(self.dictionary_test.DICT_MULTILINE_STRING["key1"], "value1")
        self.assertEqual(self.dictionary_test.DICT_MULTILINE_STRING["key2"], "value2")
        self.assertEqual(self.dictionary_test.DICT_MULTILINE_STRING["key3"], "value3")
        self.assertEqual(len(self.dictionary_test.DICT_MULTILINE_STRING), 3)

    def test_number_dictionary(self):
        """Can it load a number dictionary?"""
        self.assertEqual(self.dictionary_test.DICT_ONE_NUMBER["key1"], 10.5)
        self.assertEqual(len(self.dictionary_test.DICT_ONE_NUMBER), 1)

    def setUp(self):
        self.dictionary_test = mwutils.Constants("dictionary_basic.const")
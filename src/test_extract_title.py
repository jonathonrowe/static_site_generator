import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_hello(self):
        md = "# Hello"
        extract = extract_title(md)
        self.assertEqual(extract, "Hello")

    def test_extract_title_exception(self):
        md = "Hello"
        with self.assertRaises(Exception):
            extract_title(md)
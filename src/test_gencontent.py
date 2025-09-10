import unittest
from src.gencontent import extract_title

class TestGenContent(unittest.TestCase):
    def test_extract_title_basic(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_extra_spaces(self):
        self.assertEqual(extract_title("#    Hello    "), "Hello")

    def test_extract_title_first_h1_wins(self):
        md = "# First\n## Second\n# Third"
        self.assertEqual(extract_title(md), "First")

    def test_extract_title_raises_without_h1(self):
        with self.assertRaises(ValueError):
            extract_title("no heading here")

if __name__ == "__main__":
    unittest.main()

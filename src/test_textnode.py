import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_URL_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC, url=None)
        node2 = TextNode("This is a text node", TextType.ITALIC, url="https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_textType_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)


    def test_Text_not_eq(self):
        node = TextNode("This not a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()

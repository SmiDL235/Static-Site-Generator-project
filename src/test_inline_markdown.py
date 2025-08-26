import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertListEqual(expected, new_nodes)


    def test_delim_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertListEqual(expected, new_nodes)

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertListEqual(expected, new_nodes)
        

    def test_nontext_nodes(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [TextNode("already bold", TextType.BOLD)]
        self.assertListEqual(expected, new_nodes)


    def test_missing_delim(self):
        node = TextNode("This is text with a **bold word", TextType.TEXT)
        
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)


    def test_multi_delim(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)

        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertListEqual(expected, new_nodes)


    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)



    def test_extract_markdown_multi_img(self):
        matches = extract_markdown_images(
            "This is text with two ![map](https://ex.com/map.png) ![cat](https://ex.com/cat.jpg)"
        )
        expected = [('map','https://ex.com/map.png'), ('cat','https://ex.com/cat.jpg')]
        self.assertListEqual(expected, matches)


    def test_extract_markdown_multi_links(self):
        matches = extract_markdown_links(
            "See [home](https://ex.com) and [docs](https://ex.com/docs)"
        )
        expected = [("home", "https://ex.com"), ("docs", "https://ex.com/docs")]
        self.assertListEqual(expected, matches)


    def test_extract_markdown_mixed(self):
        text = "Mix ![pic](/p.png) and [site](https://ex.com)"
        self.assertListEqual([("pic", "/p.png")], extract_markdown_images(text))
        self.assertListEqual([("site", "https://ex.com")], extract_markdown_links(text))

if __name__ == "__main__":
    unittest.main()

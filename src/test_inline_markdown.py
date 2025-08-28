import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
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


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    
    def test_split_images_start(self):
        node = TextNode("![a](u) tail", TextType.TEXT)
        got = split_nodes_image([node])
        want = [TextNode("a", TextType.IMAGE, "u"), TextNode(" tail", TextType.TEXT)]
        self.assertListEqual(want, got)



    
    def test_split_images_end(self):
        node = TextNode("head ![a](u)", TextType.TEXT)
        got = split_nodes_image([node])
        want = [TextNode("head ", TextType.TEXT), TextNode("a", TextType.IMAGE, "u")]
        self.assertListEqual(want, got)


    
    def test_split_images_none(self):
        node = TextNode("just text", TextType.TEXT)
        got = split_nodes_image([node])
        self.assertListEqual([node], got)



    
    def test_split_images_adjacent(self):
        node = TextNode("x ![a](u)![b](v) y", TextType.TEXT)
        got = split_nodes_image([node])
        want = [
            TextNode("x ", TextType.TEXT),
            TextNode("a", TextType.IMAGE, "u"),
            TextNode("b", TextType.IMAGE, "v"),
            TextNode(" y", TextType.TEXT),
        ]
        self.assertListEqual(want, got)






    def test_split_images_passthrough_non_text(self):
        node = TextNode("![a](u)", TextType.BOLD)
        got = split_nodes_image([node])
        self.assertListEqual([node], got)





    def test_split_links_middle(self):
        node = TextNode("before [t](u) after", TextType.TEXT)
        got = split_nodes_link([node])
        want = [
            TextNode("before ", TextType.TEXT),
            TextNode("t", TextType.LINK, "u"),
            TextNode(" after", TextType.TEXT),
        ]
        self.assertListEqual(want, got)





    def test_split_links_start(self):
        node = TextNode("[t](u) tail", TextType.TEXT)
        got = split_nodes_link([node])
        want = [TextNode("t", TextType.LINK, "u"), TextNode(" tail", TextType.TEXT)]
        self.assertListEqual(want, got)





    def test_split_links_end(self):
        node = TextNode("head [t](u)", TextType.TEXT)
        got = split_nodes_link([node])
        want = [TextNode("head ", TextType.TEXT), TextNode("t", TextType.LINK, "u")]
        self.assertListEqual(want, got)






    def test_split_links_adjacent(self):
        node = TextNode("x [a](u)[b](v) y", TextType.TEXT)
        got = split_nodes_link([node])
        want = [
            TextNode("x ", TextType.TEXT),
            TextNode("a", TextType.LINK, "u"),
            TextNode("b", TextType.LINK, "v"),
            TextNode(" y", TextType.TEXT),
        ]
        self.assertListEqual(want, got)







    def test_split_links_none(self):
        node = TextNode("just text", TextType.TEXT)
        got = split_nodes_link([node])
        self.assertListEqual([node], got)




    def test_split_links_passthrough_non_text(self):
        node = TextNode("[t](u)", TextType.ITALIC)
        got = split_nodes_link([node])
        self.assertListEqual([node], got)



if __name__ == "__main__":
    unittest.main()

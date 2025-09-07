import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links, text_to_textnodes
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
        new_nodes = split_nodes_images([node])
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
        got = split_nodes_images([node])
        want = [TextNode("a", TextType.IMAGE, "u"), TextNode(" tail", TextType.TEXT)]
        self.assertListEqual(want, got)



    
    def test_split_images_end(self):
        node = TextNode("head ![a](u)", TextType.TEXT)
        got = split_nodes_images([node])
        want = [TextNode("head ", TextType.TEXT), TextNode("a", TextType.IMAGE, "u")]
        self.assertListEqual(want, got)


    
    def test_split_images_none(self):
        node = TextNode("just text", TextType.TEXT)
        got = split_nodes_images([node])
        self.assertListEqual([node], got)



    
    def test_split_images_adjacent(self):
        node = TextNode("x ![a](u)![b](v) y", TextType.TEXT)
        got = split_nodes_images([node])
        want = [
            TextNode("x ", TextType.TEXT),
            TextNode("a", TextType.IMAGE, "u"),
            TextNode("b", TextType.IMAGE, "v"),
            TextNode(" y", TextType.TEXT),
        ]
        self.assertListEqual(want, got)






    def test_split_images_passthrough_non_text(self):
        node = TextNode("![a](u)", TextType.BOLD)
        got = split_nodes_images([node])
        self.assertListEqual([node], got)





    def test_split_links_middle(self):
        node = TextNode("before [t](u) after", TextType.TEXT)
        got = split_nodes_links([node])
        want = [
            TextNode("before ", TextType.TEXT),
            TextNode("t", TextType.LINK, "u"),
            TextNode(" after", TextType.TEXT),
        ]
        self.assertListEqual(want, got)





    def test_split_links_start(self):
        node = TextNode("[t](u) tail", TextType.TEXT)
        got = split_nodes_links([node])
        want = [TextNode("t", TextType.LINK, "u"), TextNode(" tail", TextType.TEXT)]
        self.assertListEqual(want, got)





    def test_split_links_end(self):
        node = TextNode("head [t](u)", TextType.TEXT)
        got = split_nodes_links([node])
        want = [TextNode("head ", TextType.TEXT), TextNode("t", TextType.LINK, "u")]
        self.assertListEqual(want, got)






    def test_split_links_adjacent(self):
        node = TextNode("x [a](u)[b](v) y", TextType.TEXT)
        got = split_nodes_links([node])
        want = [
            TextNode("x ", TextType.TEXT),
            TextNode("a", TextType.LINK, "u"),
            TextNode("b", TextType.LINK, "v"),
            TextNode(" y", TextType.TEXT),
        ]
        self.assertListEqual(want, got)







    def test_split_links_none(self):
        node = TextNode("just text", TextType.TEXT)
        got = split_nodes_links([node])
        self.assertListEqual([node], got)




    def test_split_links_passthrough_non_text(self):
        node = TextNode("[t](u)", TextType.ITALIC)
        got = split_nodes_links([node])
        self.assertListEqual([node], got)




class TestTexttoTextNodes(unittest.TestCase):
    def test_plain_text_only(self):
        input_text = "Just some plain words."
        nodes = text_to_textnodes(input_text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "Just some plain words.")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertIsNone(nodes[0].url)


    def test_bold_only(self):
        input_text = "a **b** c"
        nodes = text_to_textnodes(input_text)

        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "a ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

        self.assertEqual(nodes[1].text, "b")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)

        self.assertEqual(nodes[2].text, " c")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)


    def test_italic_only(self):
        input_text = "a _b_ c"
        nodes = text_to_textnodes(input_text)

        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "a ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

        self.assertEqual(nodes[1].text, "b")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)

        self.assertEqual(nodes[2].text, " c")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)


    def test_image_only(self):
        input_text = "pic ![obi](https://i.imgur.com/fJRm4Vk.jpeg)"
        nodes = text_to_textnodes(input_text)

        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "pic ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

        self.assertEqual(nodes[1].text, "obi")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "https://i.imgur.com/fJRm4Vk.jpeg")


    def test_link_only(self):
        input_text = "see [boot](https://boot.dev)"
        nodes = text_to_textnodes(input_text)

        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "see ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

        self.assertEqual(nodes[1].text, "boot")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "https://boot.dev")


    def test_mixedFormatting(self):
        input_text = "This is **bold** and _ital_, `code`, ![img](https://x/y.jpg), and a [link](https://boot.dev)"
        nodes = text_to_textnodes(input_text)

        self.assertEqual(len(nodes), 10)

        self.assertEqual((nodes[0].text, nodes[0].text_type), ("This is ", TextType.TEXT))
        self.assertEqual((nodes[1].text, nodes[1].text_type), ("bold", TextType.BOLD))
        self.assertEqual((nodes[2].text, nodes[2].text_type), (" and ", TextType.TEXT))
        self.assertEqual((nodes[3].text, nodes[3].text_type), ("ital", TextType.ITALIC))
        self.assertEqual((nodes[4].text, nodes[4].text_type), (", ", TextType.TEXT))
        self.assertEqual((nodes[5].text, nodes[5].text_type), ("code", TextType.CODE))
        self.assertEqual((nodes[6].text, nodes[6].text_type), (", ", TextType.TEXT))
        self.assertEqual((nodes[7].text, nodes[7].text_type, nodes[7].url), ("img", TextType.IMAGE, "https://x/y.jpg"))
        self.assertEqual((nodes[8].text, nodes[8].text_type), (", and a ", TextType.TEXT))
        self.assertEqual((nodes[9].text, nodes[9].text_type, nodes[9].url), ("link", TextType.LINK, "https://boot.dev"))
        











if __name__ == "__main__":
    unittest.main()

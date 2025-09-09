
from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node
import unittest

class TestMarkdownBlocks(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_basic_split(self):
        md = "A\n\nB"
        self.assertEqual(markdown_to_blocks(md), ["A", "B"])


    def test_heading(self):
        self.assertEqual(block_to_block_type("### Title"), BlockType.HEADING)

    def test_code(self):
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> a\n> b"), BlockType.QUOTE)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- a\n- b"), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. a\n2. b"), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("just text"), BlockType.PARAGRAPH)


    def test_paragraph_html(self):
        md = "This is **bold** and _italic_ with `code`"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><p>This is <b>bold</b> and <i>italic</i> with <code>code</code></p></div>")

    def test_codeblock_html(self):
        md = "```\na _b_ **c**\n```\n"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><pre><code>a _b_ **c**\n</code></pre></div>")

    def test_heading_html(self):
        md = "# Hello **world**"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><h1>Hello <b>world</b></h1></div>")

    def test_quote_html(self):
        md = "> line one\n> line _two_"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><blockquote>line one line <i>two</i></blockquote></div>")

    def test_ul_html(self):
        md = "- a\n- b **bold**"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><ul><li>a</li><li>b <b>bold</b></li></ul></div>")

    def test_ol_html(self):
        md = "1. first\n2. second _it_"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><ol><li>first</li><li>second <i>it</i></li></ol></div>")

    def test_assignment_example(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>", 
        )

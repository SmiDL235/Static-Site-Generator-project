
from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type
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

import unittest
from markdown_to_blocks import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        md2 = """
# This is **bolded** heading



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        blocks2 = markdown_to_blocks(md2)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        self.assertEqual(
            blocks2,
            [
                "# This is **bolded** heading",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items"
            ]
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_heading(self):
        md = "# This is a heading"
        md2 = "## This is a second heading"
        md3 = "### This is a third heading"
        md4 = "#### This is a fourth heading"
        md5 = "##### This is a fifth heading"
        md6 = "###### This is a sixth heading"
        md7 = "####### This is an error heading"
        block_type = block_to_block_type(md)
        block_type2 = block_to_block_type(md2)
        block_type3 = block_to_block_type(md3)
        block_type4 = block_to_block_type(md4)
        block_type5 = block_to_block_type(md5)
        block_type6= block_to_block_type(md6)
        block_type7 = block_to_block_type(md7)
        self.assertEqual(block_type, BlockType.HEADING)
        self.assertEqual(block_type2, BlockType.HEADING)
        self.assertEqual(block_type3, BlockType.HEADING)
        self.assertEqual(block_type4, BlockType.HEADING)
        self.assertEqual(block_type5, BlockType.HEADING)
        self.assertEqual(block_type6, BlockType.HEADING)
        self.assertEqual(block_type7, BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        md = "```\nThis is code block```"
        md2 = "```\nThis is code block\nwith two lines```"
        md3 = "`\nThis is error code block```"
        md4 = "``\nThis is error code block```"
        md5 = "```\nThis is error code block``"
        md6 = "```This is error code block```"
        block_type = block_to_block_type(md)
        block_type2 = block_to_block_type(md2)
        block_type3 = block_to_block_type(md3)
        block_type4 = block_to_block_type(md4)
        block_type5 = block_to_block_type(md5)
        block_type6 = block_to_block_type(md6)
        self.assertEqual(block_type, BlockType.CODE)
        self.assertEqual(block_type2, BlockType.CODE)
        self.assertEqual(block_type3, BlockType.PARAGRAPH)
        self.assertEqual(block_type4, BlockType.PARAGRAPH)
        self.assertEqual(block_type5, BlockType.PARAGRAPH)
        self.assertEqual(block_type6, BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        md = "> This is a quote block"
        md2 = "> This is a quote block\n> with another block"
        md3 = "> This is a quote block\n< with an error quote block"
        md4 = "< This is an error block"
        md5 = "< This is an error block\n > with a quote block"
        block_type = block_to_block_type(md)
        block_type2 = block_to_block_type(md2)
        block_type3 = block_to_block_type(md3)
        block_type4 = block_to_block_type(md4)
        block_type5 = block_to_block_type(md5)
        self.assertEqual(block_type, BlockType.QUOTE)
        self.assertEqual(block_type2, BlockType.QUOTE)
        self.assertEqual(block_type3, BlockType.PARAGRAPH)
        self.assertEqual(block_type4, BlockType.PARAGRAPH)
        self.assertEqual(block_type5, BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered(self):
        md = "- This is an unordered list"
        md2 = "- This is an unordered list\n- with another element"
        md3 = "-This is an error block"
        block_type = block_to_block_type(md)
        block_type2 = block_to_block_type(md2)
        block_type3 = block_to_block_type(md3)
        self.assertEqual(block_type, BlockType.UNORDERED)
        self.assertEqual(block_type2, BlockType.UNORDERED)
        self.assertEqual(block_type3, BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered(self):
        md = "1. This is an ordered list"
        md2 = "1. This is an ordered list\n2. with two elements"
        md3 = "1. This is an ordered list\n3. with an error"
        md4 = "0. This is an error"
        block_type = block_to_block_type(md)
        block_type2 = block_to_block_type(md2)
        block_type3 = block_to_block_type(md3)
        block_type4 = block_to_block_type(md4)
        self.assertEqual(block_type, BlockType.ORDERED)
        self.assertEqual(block_type2, BlockType.ORDERED)
        self.assertEqual(block_type3, BlockType.PARAGRAPH)
        self.assertEqual(block_type4, BlockType.PARAGRAPH)
    
    def test_block_to_block_type_ordered(self):
        md = "This is a paragraph"
        md2 = " This is also a paragraph"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        block_type2 = block_to_block_type(md2)
        self.assertEqual(block_type2, BlockType.PARAGRAPH)
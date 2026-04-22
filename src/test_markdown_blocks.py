import unittest
from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
# This is a heading


    This is a paragraph


    - This is a list
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph",
                "- This is a list",
            ],
        )

    def test_markdown_to_blocks_whitespace(self):
        md = """
    Block 1   


    Block 2
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Block 1", "Block 2"],
        )

    def test_markdown_to_blocks_single(self):
        md = "Just a single line."
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Just a single line."],
        )

    def test_markdown_to_blocks_empty(self):
        md = """

 
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        )

    def test_headings(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Level 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Level 6"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)

    def test_code_block(self):
        code = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)
        self.assertEqual(block_to_block_type("```code```"), BlockType.PARAGRAPH)

    def test_quote_blocks(self):
        quote = "> Line 1\n> Line 2\n> Line 3"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)
        bad_quote = "> Line 1\nLine 2\n> Line 3"
        self.assertEqual(block_to_block_type(bad_quote), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        ulist = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(ulist), BlockType.UNORDERED_LIST)
        bad_ulist = "-Item 1\n-Item 2"
        self.assertEqual(block_to_block_type(bad_ulist), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        olist = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(olist), BlockType.ORDERED_LIST)
        bad_olist = "1. First\n3. Second"
        self.assertEqual(block_to_block_type(bad_olist), BlockType.PARAGRAPH)
        bad_olist2 = "2. First\n3. Second"
        self.assertEqual(block_to_block_type(bad_olist2), BlockType.PARAGRAPH)

    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("Just a normal paragraph."), BlockType.PARAGRAPH
        )


if __name__ == "__main__":
    unittest.main()

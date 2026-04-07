import unittest
from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "bolded")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

    def test_delim_italic(self):
        node = TextNode("This is text with a _italicized_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "italicized")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)

    def test_delim_bold_double(self):
        node = TextNode("This has **bold** and **more bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[3].text, "more bold")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)

    def test_delim_bold_start(self):
        node = TextNode("**Bold** at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)

    def test_delim_code(self):
        node = TextNode("This is `code` block", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)

    def test_delim_unclosed(self):
        node = TextNode("This is **bold but no end", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_delim_ignore_non_text(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "already bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

    def test_delim_mixed(self):
        node1 = TextNode("This is `code` text", TextType.TEXT)
        node2 = TextNode("this is already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("This is plain test with no images.")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("This is plain text with no links.")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images("This is ![one](url1) and ![two](url2)")
        self.assertListEqual([("one", "url1"), ("two", "url2")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "Check [Google](https://google.com) and [YouTube](https://youtube.com)"
        )
        self.assertListEqual(
            [("Google", "https://google.com"), ("YouTube", "https://youtube.com")],
            matches,
        )

    def test_extract_markdown_mixed(self):
        text = "An ![image](url_img) and a [link](url_link)"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)

        self.assertListEqual([("image", "url_img")], images)
        self.assertListEqual([("link", "url_link")], links)

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

    def test_split_links(self):
        node = TextNode(
            "Check out [Google](https://google.com) and [YouTube](https://youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check out ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("YouTube", TextType.LINK, "https://youtube.com"),
            ],
            new_nodes,
        )

    def test_split_links_at_start(self):
        node = TextNode(
            "[Google](https://google.com) is a search engine", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode(" is a search engine", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_at_start(self):
        node = TextNode(
            "![dog](https://dog.com/big_dog.png) is an image of a dog", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("dog", TextType.IMAGE, "https://dog.com/big_dog.png"),
                TextNode(" is an image of a dog", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_at_end(self):
        node = TextNode(
            "Here is an image: ![cat](https://cats.com/cat.jpg)", TextType.TEXT
        )
        new_node = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Here is an image: ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "https://cats.com/cat.jpg"),
            ],
            new_node,
        )

    def test_split_links_at_end(self):
        node = TextNode("Click here: [Google](https://google.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Click here: ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://google.com"),
            ],
            new_nodes,
        )

    def test_split_links_none(self):
        node = TextNode("This is plain text, no links here", TextType)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_none(self):
        node = TextNode("This is plain text, no images here", TextType)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_ignore_others(self):
        node = TextNode("Google", TextType.LINK, "https//google.com")
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_ignore_others(self):
        node = TextNode("cat", TextType.IMAGE, "https//cat.com/big_cat")
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_adjacent(self):
        text = "**bold**_italic_`code`"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code", TextType.CODE),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_reverse_order(self):
        text = "[link](url) then **bold**"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "url"),
                TextNode(" then ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_only_link(self):
        text = "[only link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("only link", TextType.LINK, "https://boot.dev")], new_nodes
        )

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


if __name__ == "__main__":
    unittest.main()

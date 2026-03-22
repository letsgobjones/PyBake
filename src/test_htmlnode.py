import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "Go to Website", None, {"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_values(self):
        node = HTMLNode("div", "I am a value")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "I am a value")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_multiple_props(self):
        node = HTMLNode(
            "a",
            "Go to Website",
            None,
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_no_props(self):
        node = HTMLNode("a", "Go to Website", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty(self):
        node = HTMLNode("a", "Go to Website", None, {})
        self.assertEqual(node.props_to_html(), "")


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Just some plain text")
        self.assertEqual(node.to_html(), "Just some plain text")

    def test_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_empty_value(self):
        node = LeafNode("p", "")
        self.assertEqual(node.to_html(), "<p></p>")

    def test_to_html_with_props(self):
        props = {
            "id": "main-btn",
            "class": "primary",
        }
        node = LeafNode("button", "Click Me", props)
        self.assertEqual(
            node.to_html(), '<button id="main-btn" class="primary">Click Me</button>'
        )


if __name__ == "__main__":
    unittest.main()

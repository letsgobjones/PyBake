import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()

import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_multiple_children(self):
        parent_node = ParentNode(
            "div",
            [
                LeafNode("b", "Bold"),
                LeafNode(None, "Normal"),
                LeafNode("i", "Italiic"),
            ],
        )
        self.assertEqual(
            parent_node.to_html(), "<div><b>Bold</b>Normal<i>Italiic</i></div>"
        )

    def test_to_html_deep_nesting(self):
        leaf = LeafNode("span", "Bottom")
        level2 = ParentNode("div", [leaf])
        level1 = ParentNode("div", [level2])
        root = ParentNode("div", [level1])
        self.assertEqual(
            root.to_html(), "<div><div><div><span>Bottom</span></div></div></div>"
        )

    def test_to_html_mixed_children(self):
        node = ParentNode(
            "p",
            [LeafNode(None, "Hello "), ParentNode("b", [LeafNode(None, "World")])],
        )
        self.assertEqual(node.to_html(), "<p>Hello <b>World</b></p>")

    def test_to_html_parent_with_props(self):
        node = ParentNode(
            "div", [LeafNode("span", "hi")], {"id": "main", "class": "container"}
        )
        self.assertEqual(
            node.to_html(), '<div id="main" class="container"><span>hi</span></div>'
        )


if __name__ == "__main__":
    unittest.main()

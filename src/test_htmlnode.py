import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "Boot.dev",
            props={"href": "https://boot.dev", "target": "_blank"},
        )
        expected_string = ' href="https://boot.dev" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_string)

    def test_no_props(self):
        node = HTMLNode("p", "hello")
        expected_string = ""
        self.assertEqual(node.props_to_html(), expected_string)

    def test_repr(self):
        node = HTMLNode("p", "hello")
        rep = repr(node)
        self.assertIn("p", rep)
        self.assertIn("hello", rep)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_props(self):
        node = LeafNode("a", "Hello, Boot.dev!", props={"href": "https://boot.dev"})
        expected = f'<a href="https://boot.dev">Hello, Boot.dev!</a>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_raw_text(self):
        node = LeafNode(None, "Hello")
        expected = "Hello"
        self.assertEqual(node.to_html(), expected)
    
    def test_leaf_to_html_value_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
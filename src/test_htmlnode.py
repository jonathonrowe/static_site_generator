import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

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

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode(None, "child2")
        parent_node = ParentNode("div", [child_node])
        parent_node2 = ParentNode("div", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        self.assertEqual(parent_node2.to_html(), "<div><span>child</span>child2</div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )
    
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"href": "https://boot.dev"})
        self.assertEqual(
            parent_node.to_html(),
            '<div href="https://boot.dev"><span>child</span></div>'
        )

    def test_to_html_without_children(self):
        parent_node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_without_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_without_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span></div>"
        )

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")
    
    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, {"href": "https://boot.dev"})
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href":"https://boot.dev"})
    
    def test_img(self):
        node = TextNode(
            "This is a img node",
            TextType.IMAGE, 
            {"src": "https://pix4free.org/assets/library/2021-01-19/originals/basic.jpg", "alt": "a street sign with the word basic"}
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://pix4free.org/assets/library/2021-01-19/originals/basic.jpg", "alt": "a street sign with the word basic"})

    def test_valueerror(self):
        node = TextNode("This is a value error node", "not-a-real-type")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)
import unittest
from node_delimiter import split_nodes_delimiter
from textnode import TextType, TextNode

class TestSplitNodeDelimiter(unittest.TestCase):
    def test_split_node_delimiter_text(self):
        node = TextNode("This is text with no delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "", TextType.TEXT)
        self.assertEqual(new_nodes, [node])

    def test_split_node_delimiter_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        node2 = TextNode("This is **text** with two **bold block** words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes2 = split_nodes_delimiter([node2], "**", TextType.BOLD)
        new_nodes3 = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" word", TextType.TEXT)
            ]
        )
        self.assertEqual(
            new_nodes2,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with two ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" words", TextType.TEXT)
            ]
        )
        self.assertEqual(
            new_nodes3,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with two ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" words", TextType.TEXT)
            ]
        )

    def test_split_node_delimiter_italic(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        node2 = TextNode("This is _text_ with two _italic block_ words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        new_nodes2 = split_nodes_delimiter([node2], "_", TextType.ITALIC)
        new_nodes3 = split_nodes_delimiter([node, node2], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic block", TextType.ITALIC),
                TextNode(" word", TextType.TEXT)
            ]
        )
        self.assertEqual(
            new_nodes2,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.ITALIC),
                TextNode(" with two ", TextType.TEXT),
                TextNode("italic block", TextType.ITALIC),
                TextNode(" words", TextType.TEXT)
            ]
        )
        self.assertEqual(
            new_nodes3,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic block", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.ITALIC),
                TextNode(" with two ", TextType.TEXT),
                TextNode("italic block", TextType.ITALIC),
                TextNode(" words", TextType.TEXT)
            ]
        )

    def test_split_node_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is `text` with two `code block` words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes2 = split_nodes_delimiter([node2], "`", TextType.CODE)
        new_nodes3 = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT)
            ]
        )
        self.assertEqual(
            new_nodes2,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.CODE),
                TextNode(" with two ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" words", TextType.TEXT)
            ]
        )
        self.assertEqual(
            new_nodes3,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.CODE),
                TextNode(" with two ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" words", TextType.TEXT)
            ]
        )

    def test_split_node_delimiter_exception(self):
        node = TextNode("This is text with a **bold block* word", TextType.TEXT)
        node2 = TextNode("This is _text_ with a _italic block word", TextType.TEXT)
        node3 = TextNode("This is `text` with a` `code block` word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node2], "_", TextType.ITALIC)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node3], "`", TextType.CODE)
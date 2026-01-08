import unittest
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link
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

class TestSplitNodeImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) end",
            TextType.TEXT
        )
        node3 = TextNode("This is text without an image", TextType.TEXT)
        node4 = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        new_nodes2 = split_nodes_image([node2])
        new_nodes3 = split_nodes_image([node, node2])
        new_nodes4 = split_nodes_image([node3])
        new_nodes5 = split_nodes_image([node4])
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
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" end", TextType.TEXT)
            ],
            new_nodes2
        )
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" end", TextType.TEXT)
            ],
            new_nodes3
        )
        self.assertListEqual(
            [
                TextNode("This is text without an image", TextType.TEXT)
            ],
            new_nodes4
        )
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ), 
            ],
            new_nodes5
        )

class SplitNodeLink(unittest.TestCase):
    def test_split_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
            )
        node2 = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) website",
            TextType.TEXT,
        )
        node3 = TextNode("[to boot dev](https://www.boot.dev) website", TextType.TEXT)
        node4 = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        node5 = TextNode("This is text without a link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        new_nodes2 = split_nodes_link([node2])
        new_nodes3 = split_nodes_link([node3])
        new_nodes4 = split_nodes_link([node4])
        new_nodes5 = split_nodes_link([node5])
        new_nodes6 = split_nodes_link([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            new_nodes
        )
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" website", TextType.TEXT)
            ],
            new_nodes2
        )
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" website", TextType.TEXT),
            ],
            new_nodes3
        )
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes4
        )
        self.assertListEqual(
            [TextNode("This is text without a link", TextType.TEXT)],
            new_nodes5
        )
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" website", TextType.TEXT),
            ],
            new_nodes6
        )
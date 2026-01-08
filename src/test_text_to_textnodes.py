import unittest
from text_to_textnodes import text_to_textnodes
from textnode import TextNode, TextType

class TestTextToTextNode(unittest.TestCase):
    def test_text_to_textnode_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text2 = "This is _text_ with a **bold** word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text3 = "This is an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) with **text** and an _italic_ word and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        nodes2 = text_to_textnodes(text2)
        nodes3 = text_to_textnodes(text3)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.ITALIC),
                TextNode(" with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes2
        )
        self.assertListEqual(
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" with ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" and an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev")
            ],
            nodes3
        )

    def test_text_to_textnode_plaintext(self):
        text = "This is text without any markdown"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("This is text without any markdown", TextType.TEXT)],
            nodes
        )

    def test_text_to_textnode_onlybold(self):
        text = "This is **text** with bold"
        text2 = "This is **text** with **bold**"
        nodes = text_to_textnodes(text)
        nodes2 = text_to_textnodes(text2)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with bold", TextType.TEXT)
            ],
            nodes
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD)
            ],
            nodes2
        )

    def test_text_to_textnode_onlyitalic(self):
        text = "This is _text_ with italic"
        text2 = "This is _text_ with _italic_"
        nodes = text_to_textnodes(text)
        nodes2 = text_to_textnodes(text2)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.ITALIC),
                TextNode(" with italic", TextType.TEXT) 
            ],
            nodes
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.ITALIC),
                TextNode(" with ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC) 
            ],
            nodes2
        )
    
    def test_text_to_textnode_onlycode(self):
        text = "This is `text` with code"
        text2 = "This is `text` with `code`"
        nodes = text_to_textnodes(text)
        nodes2 = text_to_textnodes(text2)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.CODE),
                TextNode(" with code", TextType.TEXT) 
            ],
            nodes
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.CODE),
                TextNode(" with ", TextType.TEXT),
                TextNode("code", TextType.CODE)
            ],
            nodes2
        )

    def test_text_to_textnode_onlyimage(self):
        text = "This is text with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        text2 = "This is text with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a ![python image](https://imgur.com/zjjcJKZ)"
        nodes = text_to_textnodes(text)
        nodes2 = text_to_textnodes(text2)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
            ],
            nodes
        )
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("python image", TextType.IMAGE, "https://imgur.com/zjjcJKZ")
            ],
            nodes2
        )
    
    def test_text_to_textnode_onlylink(self):
        text = "This is text with a [link](https://boot.dev)"
        text2 = "This is text with a [link](https://boot.dev) and [another link](https://www.youtube.com/@bootdotdev)"
        nodes = text_to_textnodes(text)
        nodes2 = text_to_textnodes(text2)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev")
            ],
            nodes
        )
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            nodes2
        )
import unittest
from markdown_to_html_node import markdown_to_html_node

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_heading_with_inline(self):
        md = "# Title with **bold** and _italic_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title with <b>bold</b> and <i>italic</i></h1></div>",
        )

    def test_unordered_list_inline(self):
        md = "- first **bold**\n- second _italic_\n- third `code`"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul>"
            "<li>first <b>bold</b></li>"
            "<li>second <i>italic</i></li>"
            "<li>third <code>code</code></li>"
            "</ul></div>",
        )

    def test_ordered_list(self):
        md = """
    1. one
    2. two
    3. three
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol>"
            "<li>one</li>"
            "<li>two</li>"
            "<li>three</li>"
            "</ol></div>",
        )

    def test_blockquote_inline(self):
        md = """
    > This is a _quote_ with **style**
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a <i>quote</i> with <b>style</b></blockquote></div>",
        )

    def test_mixed_document(self):
        md = "# Heading\n\nParagraph with `code`.\n\n- item **one**\n- item _two_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"
            "<h1>Heading</h1>"
            "<p>Paragraph with <code>code</code>.</p>"
            "<ul>"
            "<li>item <b>one</b></li>"
            "<li>item <i>two</i></li>"
            "</ul>"
            "</div>",
        )

    def test_paragraphs_and_list(self):
        md = "First.\n\nSecond.\n\n- one\n- two"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div>"
            "<p>First.</p>"
            "<p>Second.</p>"
            "<ul><li>one</li><li>two</li></ul>"
            "</div>",
        )

    def test_multiline_blockquote(self):
        md = "> line one\n> line **two**"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>line one\nline <b>two</b></blockquote></div>",
        )
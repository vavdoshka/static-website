from markdown2html import markdown_to_html_node, block_to_html_node
from markdown import MarkdownBlockType
from htmlnode import ParentNode, LeafNode
import unittest


class TestMarkdown2html(unittest.TestCase):

    def test_block_paragraph_to_html_node_basic(self):
        block = "this is a basic test"
        self.assertEqual(
            block_to_html_node(block, MarkdownBlockType.PARAGRAPH),
            ParentNode("p", [LeafNode("", "this is a basic test")])
        )

    def test_block_paragraph_to_html_node_inline_markdown(self):
        block = "this is a basic **bold** test"
        self.assertEqual(
            block_to_html_node(block, MarkdownBlockType.PARAGRAPH),
            ParentNode("p", [LeafNode("", "this is a basic "),
                       LeafNode("b", "bold"), LeafNode("", " test")])
        )

    def test_block_paragraph_only_url(self):
        block = "[Back Home](/)"
        node = block_to_html_node(block, MarkdownBlockType.PARAGRAPH)
        print(node)
        self.assertEqual(
            node,
            ParentNode("p", [
                LeafNode("a", "Back Home", {"href": "/"})
            ])
        )

    def test_block_paragraph_only_image(self):
        block = "![LOTR image artistmonkeys](/images/rivendell.png)"
        node = block_to_html_node(block, MarkdownBlockType.PARAGRAPH)
        self.assertEqual(
            node,
            ParentNode("p", [
                LeafNode("img", "", {
                         "src": "/images/rivendell.png", "alt": "LOTR image artistmonkeys"}),
            ])
        )

    def test_block_code_to_html_node_basic(self):
        block = "```\n# some code block\n# more code\n```"
        self.assertEqual(
            block_to_html_node(block, MarkdownBlockType.CODE),
            ParentNode(
                "pre", [LeafNode("code", "# some code block\n# more code")])
        )

    def test_block_quote_to_html_node_basic(self):
        block = "> some quote"
        self.assertEqual(
            block_to_html_node(block, MarkdownBlockType.QUOTE),
            ParentNode("blockquote", [LeafNode("", "some quote")])
        )

    def test_block_quote_to_html_node_multiline_inline(self):
        block = "> some quote\n>continues with **bold** and `code`"
        self.assertEqual(
            block_to_html_node(block, MarkdownBlockType.QUOTE),
            ParentNode("blockquote", [
                       LeafNode("", "some quote\ncontinues with "),
                       LeafNode("b", "bold"),
                       LeafNode("", " and "),
                       LeafNode("code", "code"),
                       ])
        )

    def test_block_heading_to_html_node_basic(self):
        block = "### heading3"
        self.assertEqual(
            block_to_html_node(block, MarkdownBlockType.HEADING),
            ParentNode("h3", [
                LeafNode("", "heading3"),
            ])
        )

    def test_block_heading_to_html_node_inline(self):
        block = "###### heading6 with *italic*"
        self.assertEqual(
            block_to_html_node(block, MarkdownBlockType.HEADING),
            ParentNode("h6", [
                LeafNode("", "heading6 with "),
                LeafNode("i", "italic"),
            ])
        )

    def test_block_ul_to_html_node_basic(self):
        block = "* item1"
        self.assertEqual(
            block_to_html_node(block, MarkdownBlockType.UNORDERED_LIST),
            ParentNode("ul", [ParentNode("li", [
                LeafNode("", "item1"),
            ])])
        )

    def test_block_ul_to_html_node_multiline_inline(self):
        block = "* item1 *italic*\n- item2 `code` and stuff"
        self.assertEqual(
            block_to_html_node(block, MarkdownBlockType.UNORDERED_LIST),
            ParentNode("ul", [ParentNode("li", [
                LeafNode("", "item1 "),
                LeafNode("i", "italic"),
            ]),
                ParentNode("li", [
                    LeafNode("", "item2 "),
                    LeafNode("code", "code"),
                    LeafNode("", " and stuff"),
                ])
            ])
        )

    def test_block_ol_to_html_node_basic(self):
        block = "1. item1"
        self.assertEqual(
            block_to_html_node(block, MarkdownBlockType.ORDERED_LIST),
            ParentNode("ol", [ParentNode("li", [
                LeafNode("", "item1"),
            ])])
        )

    def test_block_ul_to_html_node_multiline_inline(self):
        block = "1. item1 *italic*\n2. item2 `code` and stuff"
        self.assertEqual(
            block_to_html_node(block, MarkdownBlockType.ORDERED_LIST),
            ParentNode("ol", [ParentNode("li", [
                LeafNode("", "item1 "),
                LeafNode("i", "italic"),
            ]),
                ParentNode("li", [
                    LeafNode("", "item2 "),
                    LeafNode("code", "code"),
                    LeafNode("", " and stuff"),
                ])
            ])
        )

    def test_markdown_to_html_node_end_to_end(self):
        text = """
## This is a heading with `code`

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item with [url](https://www.boot.dev) in a list block
- This is a list item with ![image](https://www.boot.dev/image.png)
* This is another list item
"""

        nodes = markdown_to_html_node(text)
        self.assertEqual(
            nodes,
            ParentNode("div", [
                ParentNode("h2", [
                    LeafNode("", "This is a heading with "),
                    LeafNode("code", "code"),
                ]),
                ParentNode("p", [
                    LeafNode("", "This is a paragraph of text. It has some "),
                    LeafNode("b", "bold"),
                    LeafNode("", " and "),
                    LeafNode("i", "italic"),
                    LeafNode("", " words inside of it."),
                ]),
                ParentNode("ul", [
                    ParentNode("li", [
                        LeafNode("", "This is the first list item with "),
                        LeafNode("a", "url", {"href": "https://www.boot.dev"}),
                        LeafNode("", " in a list block"),
                    ]),
                    ParentNode("li", [
                        LeafNode("", "This is a list item with "),
                        LeafNode(
                            "img", "", {"src": "https://www.boot.dev/image.png", "alt": "image"}),
                    ]),
                    ParentNode(
                        "li", [LeafNode("", "This is another list item")])
                ])
            ])
        )


if __name__ == "__main__":
    unittest.main()

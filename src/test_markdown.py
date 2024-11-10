import unittest
from markdown import markdown_to_blocks, text_node_to_html_code, split_nodes_delimeter, split_node, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image, text_to_textnodes, block_to_block_type, MarkdownBlockType
from textnode import TextNode, TextType
from htmlnode import LeafNode

class UtilsTests(unittest.TestCase):

    def test_text_node_to_html_code_no_type(self):
        node = TextNode("text", "")
        with self.assertRaises(ValueError):
            text_node_to_html_code(node)

    def test_text_node_to_html_code_text(self):
        node = TextNode("text", TextType.TEXT)
        self.assertEqual(text_node_to_html_code(node), LeafNode("", "text"))

    def test_text_node_to_html_code_bold(self):
        node = TextNode("bold", TextType.BOLD)
        self.assertEqual(text_node_to_html_code(node), LeafNode("b", "bold"))

    def test_text_node_to_html_code_italic(self):
        node = TextNode("italic", TextType.ITALIC)
        self.assertEqual(text_node_to_html_code(node), LeafNode("i", "italic"))

    def test_text_node_to_html_code_code(self):
        node = TextNode("somestuff", TextType.CODE)
        self.assertEqual(text_node_to_html_code(
            node), LeafNode("code", "somestuff"))

    def test_text_node_to_html_code_link(self):
        node = TextNode("link", TextType.LINK, url="https://boot.dev")
        self.assertEqual(text_node_to_html_code(node), LeafNode(
            "a", "link", {"href": "https://boot.dev"}))

    def test_text_node_to_html_code_image(self):
        node = TextNode("im", TextType.IMAGE,
                        url="https://boot.dev/im.png")
        self.assertEqual(text_node_to_html_code(node), LeafNode(
            "img", "", {"src": "https://boot.dev/im.png", "alt": "im"}))

    def test_split_node_one_occurence_middle(self):
        result = split_node("first `code` last", "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("first ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" last", TextType.TEXT)
        ])

    def test_split_node_one_occurence_bold_type(self):
        result = split_node("first **bold** last", "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("first ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" last", TextType.TEXT)
        ])

    def test_split_node_one_occurrence_begin(self):
        result = split_node("`code` first last", "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("code", TextType.CODE),
            TextNode(" first last", TextType.TEXT),
        ])

    def test_split_node_one_occurrence_end(self):
        result = split_node("first last `code`", "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("first last ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ])

    def test_split_node_no_occurrences(self):
        result = split_node("first last", "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("first last", TextType.TEXT),
        ])

    def test_split_node_inbalanced(self):
        with self.assertRaises(ValueError):
            split_node("first `last", "`", TextType.CODE)

    def test_split_node_two_occurrences(self):
        result = split_node("first `code` last `code`", "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("first ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" last ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ])

    def test_split_node_many_occurrences(self):
        result = split_node(
            "`code`first `code` last `code` a`code`here", "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("code", TextType.CODE),
            TextNode("first ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" last ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" a", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("here", TextType.TEXT),
        ])

    def test_split_node_delimeter_not_found(self):
        result = split_nodes_delimeter(
            [TextNode("This is a text with no delimeters", TextType.TEXT)],
            "`",
            TextType.CODE
        )
        self.assertEqual(result,
                         [TextNode("This is a text with no delimeters", TextType.TEXT)])

    def test_split_node_delimeter_no_text(self):
        result = split_nodes_delimeter(
            [TextNode("# This is a comment", TextType.CODE)],
            "*",
            TextType.BOLD
        )
        self.assertEqual(result,
                         [TextNode("# This is a comment", TextType.CODE)])

    def test_split_node_delimeter_code(self):
        result = split_nodes_delimeter(
            [TextNode("This is a text with a `code block` word", TextType.TEXT)],
            "`",
            TextType.CODE
        )
        self.assertEqual(result,
                         [TextNode("This is a text with a ", TextType.TEXT),
                          TextNode("code block", TextType.CODE),
                          TextNode(" word", TextType.TEXT)])

    def test_split_node_delimeter_bold_mixed(self):
        result = split_nodes_delimeter(
            [TextNode("This is a text with several **bold** **words**", TextType.TEXT),
             TextNode("# This is a code block", TextType.CODE),
             TextNode("This is a text with no match", TextType.TEXT)],
            "**",
            TextType.BOLD
        )
        self.assertEqual(result,
                         [TextNode("This is a text with several ", TextType.TEXT),
                          TextNode("bold", TextType.BOLD),
                          TextNode(" ", TextType.TEXT),
                          TextNode("words", TextType.BOLD),
                          TextNode("# This is a code block", TextType.CODE),
                          TextNode("This is a text with no match", TextType.TEXT)])

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text),
                         [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text),
                         [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_markdown_links_in_image_string(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_links(text),
                         [])

    def test_extract_markdown_links_empty_string(self):
        text = ""
        self.assertEqual(extract_markdown_links(text),
                         [])

    def test_extract_markdown_links_newlines(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) \nand [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text),
                         [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_markdown_links_mixed_with_images(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) \nand ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_links(text),
                         [("to boot dev", "https://www.boot.dev")])

    def test_extract_markdown_images_mixed_with_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) \nand ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text),
                         [("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_split_nodes_link_simply_text(self):
        node = TextNode(
            "There are no links",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [TextNode("There are no links", TextType.TEXT)]
        )

    def test_split_nodes_link_one(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) last",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [TextNode("This is text with a link ", TextType.TEXT),
             TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
             TextNode(" last", TextType.TEXT)]
        )

    def test_split_nodes_text_with_link_only(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")]
        )

    def test_split_nodes_link_two_different(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ]
        )

    def test_split_nodes_link_two_equals(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) two times [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [TextNode("This is text with a link ", TextType.TEXT),
             TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
             TextNode(" two times ", TextType.TEXT),
             TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")]
        )

    def test_split_nodes_link_multiple_nodes(self):
        nodes = [TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) two times [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        ),
            TextNode(
            "There is no url",
            TextType.TEXT,
        ),
            TextNode(
            "There is an image url ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        ),
            TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) two times [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        ),
        ]
        self.assertEqual(
            split_nodes_link(nodes),
            [TextNode("This is text with a link ", TextType.TEXT),
             TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
             TextNode(" two times ", TextType.TEXT),
             TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
             TextNode("There is no url", TextType.TEXT),
             TextNode(
                 "There is an image url ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT),
             TextNode("This is text with a link ", TextType.TEXT),
             TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
             TextNode(" two times ", TextType.TEXT),
             TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
             ]
        )

    def test_split_nodes_images_one(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and",
            TextType.TEXT,
        )

        self.assertEqual(
            split_nodes_image([node]),
            [TextNode("This is text with a ", TextType.TEXT),
             TextNode("rick roll", TextType.IMAGE,
                      "https://i.imgur.com/aKaOqIh.gif"),
             TextNode(" and", TextType.TEXT)]
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE,
                         "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

    def test_text_to_textnodes_error(self):
        text = "This is **text with an *italic* word"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)

    def test_markdown_to_blocks_base(self):
        # text = "# block1\nblock2\n*block3\n*block3"
        text = "# block1\n\nblock2\n\n*block3"
        self.assertEqual(
            markdown_to_blocks(text),
            [
                "# block1",
                "block2",
                "*block3"
            ]
        )

    def test_markdown_to_blocks_with_lists(self):
        text = "# block1\n\nblock2\n\n*block3\n*block3"
        self.assertEqual(
            markdown_to_blocks(text),
            [
                "# block1",
                "block2",
                "*block3\n*block3"
            ]
        )

    def test_markdown_to_blocks_with_lists_excessive_newlines(self):
        text = "# block1\n\n\nblock2\n\n\n*block3\n*block3\n\n"
        self.assertEqual(
            markdown_to_blocks(text),
            [
                "# block1",
                "block2",
                "*block3\n*block3"
            ]
        )

    def test_markdown_to_blocks_with_lists_several_types(self):
        text = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        self.assertEqual(
            markdown_to_blocks(text),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
            ]
        )

    def test_block_to_block_heading(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), MarkdownBlockType.HEADING)


    def test_block_to_block_heading_broken_multiline(self):
        block = "# heading1\n# heading2"
        self.assertEqual(block_to_block_type(block), MarkdownBlockType.PARAGRAPH)

    def test_block_to_block_heading_broken_many_levels(self):
        for x in range(6):
            self.assertEqual(block_to_block_type(f"{'#' * (x+1)} heading"), MarkdownBlockType.HEADING)

    def test_block_to_block_heading_no_space(self):
        block = "#######heading1"
        self.assertEqual(block_to_block_type(block), MarkdownBlockType.PARAGRAPH)
        
    def test_block_to_block_heading_empty(self):
        block = "# "
        self.assertEqual(block_to_block_type(block), MarkdownBlockType.HEADING)

    def test_block_to_block_code(self):
        block = "```\n#code\n```"
        self.assertEqual(block_to_block_type(block), MarkdownBlockType.CODE)

    def test_block_to_block_code_incomplete(self):
        block = "```\n#code"
        self.assertEqual(block_to_block_type(block), MarkdownBlockType.PARAGRAPH)

    def test_block_to_block_code_six_backticks(self):
        block = "``````"
        self.assertEqual(block_to_block_type(block), MarkdownBlockType.PARAGRAPH)

    def test_block_to_block_quotes(self):
        block = ">this is\n> some famous quote"
        self.assertEqual(block_to_block_type(block), MarkdownBlockType.QUOTE)

    def test_block_to_block_quotes_broken(self):
        block = ">this is\n> some famous quote\nwhich is broken"
        self.assertEqual(block_to_block_type(block), MarkdownBlockType.PARAGRAPH)

    def test_block_to_block_quotes_empty(self):
        block = ">"
        self.assertEqual(block_to_block_type(block), MarkdownBlockType.QUOTE)

    def test_block_to_block_ul(self):
        block = "- one\n* two\n- three"
        self.assertEqual(block_to_block_type(block), MarkdownBlockType.UNORDERED_LIST)

    def test_block_to_block_ul_broken(self):
        block = "- one\n* two\n-three"
        self.assertEqual(block_to_block_type(block), MarkdownBlockType.PARAGRAPH)

    def test_block_to_block_ol(self):
        block = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(block), MarkdownBlockType.ORDERED_LIST)

    def test_block_to_block_ol_broken(self):
        block = "1. one\n2. two\n4.three"
        self.assertEqual(block_to_block_type(block), MarkdownBlockType.PARAGRAPH)

    def test_block_to_block_paragraph(self):
        block = "simple paragraph"
        self.assertEqual(block_to_block_type(block), MarkdownBlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()

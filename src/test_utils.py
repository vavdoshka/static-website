import unittest
from utils import text_node_to_html_code, split_nodes_delimeter, split_node, extract_markdown_images, extract_markdown_links
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
        node = TextNode("code", TextType.CODE)
        self.assertEqual(text_node_to_html_code(node), LeafNode("code", "code"))

    def test_text_node_to_html_code_link(self):
        node = TextNode("link", TextType.LINK, url="https://boot.dev")
        self.assertEqual(text_node_to_html_code(node), LeafNode("a", "link", {"href": "https://boot.dev"}))

    def test_text_node_to_html_code_image(self):
        node = TextNode("img", TextType.IMAGE, url="https://boot.dev/image.png")
        self.assertEqual(text_node_to_html_code(node), LeafNode("img", "", {"src": "https://boot.dev/image.png", "alt": "img"}))

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
        result = split_node("`code`first `code` last `code` a`code`here", "`", TextType.CODE)
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
        
if __name__ == "__main__":
    unittest.main()
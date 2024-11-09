from htmlnode import HTMLNode, LeafNode, ParentNode
import unittest


class HtmlNodeTests(unittest.TestCase):

    def test_repr(self):
        node = HTMLNode("tag", "value", "children", "props")
        self.assertEqual(repr(node), "HTMLNode(tag, value, children, props)")

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.boot.dev\" target=\"_blank\"")

    def test_to_html(self):
        node = HTMLNode("tag", "value", "children", "props")
        self.assertRaises(NotImplementedError, node.to_html)

    def test_leaf_node_to_html_no_value(self):
        node = LeafNode("a", "")
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_node_to_html_no_tag(self):
        node = LeafNode("", "value")
        self.assertEqual(node.to_html(), "value")

    def test_leaf_node_to_html(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.boot.dev\">Click me!</a>")

    def test_parent_node_to_html_no_tag(self):
        node = ParentNode("", ["1"])
        self.assertRaises(ValueError, node.to_html)

    def test_parent_node_to_html_no_children(self):
        node = ParentNode("1", [])
        self.assertRaises(ValueError, node.to_html)


    def test_parent_node_to_html_one_children(self):
        node = ParentNode("p", [LeafNode("p", "simple text")])
        self.assertEqual(node.to_html(), 
                         "<p><p>simple text</p></p>")
        
    def test_parent_node_to_html_many_children(self):
        node = ParentNode("p", [LeafNode("p", "simple text"), LeafNode("p", "simple text")], props={"fake": "prop"})
        self.assertEqual(node.to_html(), 
                         "<p fake=\"prop\"><p>simple text</p><p>simple text</p></p>")

    def test_parent_node_to_html_nested_parent(self):
        node = ParentNode("p", [ParentNode("p", [LeafNode("h1", "simple text")])])
        self.assertEqual(node.to_html(), 
                         "<p><p><h1>simple text</h1></p></p>")

    def test_parent_node_to_html_mix_parent_and_leaf(self):
        node = ParentNode("p",
                           [LeafNode("h1", "heading"),
                             ParentNode("p", [LeafNode("h2", "heading"),
                              ParentNode("p", [LeafNode("h4", "heading")])]), 
                              LeafNode(None, "trailing")])
        self.assertEqual(node.to_html(), 
                         "<p><h1>heading</h1><p><h2>heading</h2><p><h4>heading</h4></p></p>trailing</p>")

if __name__ == "__main__":
    unittest.main()

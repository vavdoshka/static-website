import re

from textnode import TextType, TextNode
from htmlnode import LeafNode

def text_node_to_html_code(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode("", text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", "code")
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": "https://boot.dev/image.png", "alt": "img"})
        case _:
            raise ValueError(f"unknow type: \"{text_node.text_type}\"")


def split_node(string, delimeter, textType):
    
    result = []
    stack = []
    tail_index = 0
    for i in range(len(string)):
        if string[i:i+len(delimeter)] == delimeter:
            if not stack:
                if string[tail_index:i]:
                    result.append(TextNode(string[tail_index:i], TextType.TEXT))
                stack.append(i + len(delimeter))
                tail_index = i + len(delimeter)
            else:
                openning_pos = stack.pop()
                result.append(TextNode(string[openning_pos:i], textType))
                tail_index = i + len(delimeter)
    if stack:
        raise ValueError(f"Delimeter {delimeter} is not properly closed")
    if string[tail_index:]:
        result.append(TextNode(string[tail_index:], TextType.TEXT))
    return result

def split_nodes_delimeter(old_nodes, delimeter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            result.extend(split_node(node.text, delimeter, text_type))
        else:
            result.append(node)
    return result            
            
def extract_markdown_images(text):
    return re.findall("!\[([^\]\[]+)\]\((\S+)\)", text)

def extract_markdown_links(text):
    return re.findall("[^!]\[([^\]\[]+)\]\((\S+)\)", text)
            
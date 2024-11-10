import re

from textnode import TextType, TextNode
from htmlnode import LeafNode
from enum import Enum

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
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"unknow type: \"{text_node.text_type}\"")


def split_node(text, delimeter, textType):
    
    result = []
    stack = []
    tail_index = 0
    for i in range(len(text)):
        if text[i:i+len(delimeter)] == delimeter:
            if not stack:
                if text[tail_index:i]:
                    result.append(TextNode(text[tail_index:i], TextType.TEXT))
                stack.append(i + len(delimeter))
                tail_index = i + len(delimeter)
            else:
                openning_pos = stack.pop()
                result.append(TextNode(text[openning_pos:i], textType))
                tail_index = i + len(delimeter)
    if stack:
        raise ValueError(f"Delimeter {delimeter} is not properly closed")
    if text[tail_index:]:
        result.append(TextNode(text[tail_index:], TextType.TEXT))
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
            
def split_link(text, patterns, textType):

    if not text:
        return []
    
    if not patterns:
        return [TextNode(text, TextType.TEXT)]
    
    pattern = patterns[0]
    template = ""
    match textType:
        case TextType.IMAGE:
            template = f"![{pattern[0]}]({pattern[1]})"
        case TextType.LINK:
            template = f"[{pattern[0]}]({pattern[1]})"
        case _:
            raise ValueError(f"Unknown parsing type: {_}")
    sections = text.split(template, 1)

    if len(sections) == 1:
        return [TextNode(text, TextType.TEXT)]

    result = []

    result.extend(split_link(sections[0], patterns[1:], textType))
    result.append(TextNode(pattern[0], textType, pattern[1]))
    result.extend(split_link(sections[1], patterns[1:], textType))

    return result

def split_nodes_regexp(old_nodes, regex_extractor, textType):
    result = []
    for node in old_nodes:
        patterns = regex_extractor(node.text)
        if not patterns:
            result.append(node)
        else:
            result.extend(split_link(node.text, patterns, textType))
    return result

def split_nodes_link(old_nodes):
    return split_nodes_regexp(old_nodes, extract_markdown_links, TextType.LINK)

def split_nodes_image(old_nodes):
    return split_nodes_regexp(old_nodes, extract_markdown_images, TextType.IMAGE)

def text_to_textnodes(text):
    result = [
        TextNode(text, TextType.TEXT)
    ]

    result = split_nodes_delimeter(result, "**", TextType.BOLD)
    result = split_nodes_delimeter(result, "*", TextType.ITALIC)
    result = split_nodes_delimeter(result, "`", TextType.CODE)
    result = split_nodes_image(result)
    result = split_nodes_link(result)

    return result

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


class MarkdownBlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def test_block_type(line, block_type, index=None):
    match block_type:
        case block_type.HEADING:
            return index == 0 and (line.startswith("# ") or line.startswith("## ") or line.startswith("### ") or\
                line.startswith("#### ") or line.startswith("##### ") or line.startswith("###### "))
        case block_type.CODE:
            return line.strip() == "```"
        case block_type.QUOTE:
            return line.startswith(">")
        case block_type.UNORDERED_LIST:
            return line.startswith("* ") or line.startswith("- ")
        case block_type.ORDERED_LIST:
            return line.startswith(f"{index + 1}. ")
        case _:
            raise ValueError(f"Unknown value: {_}")

def block_to_block_type(block):
    lines = block.split("\n")
    block_type = None

    if test_block_type(lines[0], MarkdownBlockType.CODE) and test_block_type(lines[-1], MarkdownBlockType.CODE):
        return MarkdownBlockType.CODE
    
    if test_block_type(lines[0], MarkdownBlockType.HEADING, index=0):
        block_type = MarkdownBlockType.HEADING
    elif test_block_type(lines[0], MarkdownBlockType.QUOTE):
        block_type = MarkdownBlockType.QUOTE
    elif test_block_type(lines[0], MarkdownBlockType.UNORDERED_LIST):
        block_type = MarkdownBlockType.UNORDERED_LIST
    elif test_block_type(lines[0], MarkdownBlockType.ORDERED_LIST, index=0):
        block_type = MarkdownBlockType.ORDERED_LIST
    else:
        return MarkdownBlockType.PARAGRAPH

    for i, l in enumerate(lines):
        if not test_block_type(l, block_type, index=i):
            return MarkdownBlockType.PARAGRAPH
        
    return block_type
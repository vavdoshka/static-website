from enum import Enum
from htmlnode import ParentNode, LeafNode

from markdown import markdown_to_blocks, text_to_textnodes, block_to_block_type, MarkdownBlockType, text_node_to_html_code
from textnode import TextType

def text_type_to_html(text_type):
    return {
        TextType.BOLD: "b",
        TextType.TEXT: "p",

    }.get(text_type)


# OL / UL

# CODE - no touch

# def convert_to_block_html_node(block, block_type):

#     match block_type:
#         case MarkdownBlockType.

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    result = []
    for node in text_nodes:
        result.append(text_node_to_html_code(node))
    return result

def block_to_paragraph(block):
    children = text_to_children(block)
    return ParentNode("p", children)

def block_to_code(block):
    raw_lines = block.split("\n")
    code = "\n".join(raw_lines[1:-1])
    return ParentNode("pre", [LeafNode("code", code)])

def block_to_quote(block):
    raw_lines = block.split("\n")
    quote = "\n".join([l.lstrip("> ").lstrip(">") for l in raw_lines])
    children = text_to_children(quote)
    return ParentNode("blockquote", [ParentNode("p", children)])

def block_to_heading(block):
    # get number of h, strip, pass to text_to_children, wrap with h tag
    hcount = len(block.split(" ", 1)[0])
    header_text = block[hcount+1:]
    children = text_to_children(header_text)
    return ParentNode(f"h{hcount}", children)

def block_to_list(block, lstrip_length):
    lines = block.split("\n")
    items = []
    for l in lines:
        text = l[lstrip_length:]
        children = text_to_children(text)
        items.append(
            ParentNode("li", children)
        )
    return items

def block_to_ul(block):
    items = block_to_list(block, 2)
    return ParentNode("ul", items)

def block_to_ol(block):
    items = block_to_list(block, 3)
    return ParentNode("ol", items)

def block_to_html_node(block, block_type):
    match block_type:
        case MarkdownBlockType.PARAGRAPH:
            return block_to_paragraph(block)
        case MarkdownBlockType.CODE:
            return block_to_code(block)
        case MarkdownBlockType.QUOTE:
            return block_to_quote(block)
        case MarkdownBlockType.HEADING:
            return block_to_heading(block)
        case MarkdownBlockType.UNORDERED_LIST:
            return block_to_ul(block)
        case MarkdownBlockType.ORDERED_LIST:
            return block_to_ol(block)

def markdown_to_html_node(markdown):
    tree = []

    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)
        tree.append(block_to_html_node(block, block_type))
        
    return ParentNode("div", tree)
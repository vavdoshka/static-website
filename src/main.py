from textnode import TextNode, NodeType
def main():
    text_node = TextNode("This is a text node", NodeType.BOLD, "https://www.boot.dev")
    print(text_node)

main()
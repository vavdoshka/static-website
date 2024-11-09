class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        props = []
        if not self.props:
            return ""
        for k,v in self.props.items():
            props.append(f"{k}=\"{v}\"")
        return " " + " ".join(props)
    
    def __eq__(self, value):
        return value.tag == self.tag and\
            value.value == self.value and\
            value.children == self.children and\
            value.props == self.props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        buffer = []
        for child in self.children:
            buffer.append(child.to_html())
        return f"<{self.tag}{self.props_to_html()}>" + ''.join(buffer) + f"</{self.tag}>"

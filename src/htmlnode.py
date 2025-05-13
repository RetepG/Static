from textnode import TextNode, TextType

class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses must implement the to_html() method.")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        
        list_prop = []
        for key, value in self.props.items():
            combined = f' {key}="{value}"'
            list_prop.append(combined)
        return "".join(list_prop)
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag = tag, value = value, children = None, props = props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag = tag, value = None, children = children, props = props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        
        if self.children is None:
            raise ValueError("All parent nodes must have a children")
        
        string_format = f"<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            string_format += child.to_html()
        
        string_format += f"</{self.tag}>"

        return string_format
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
        

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.NORMAL_TEXT:
        node = LeafNode(None, text_node.text, None)
        return node
    elif text_node.text_type == TextType.BOLD_TEXT:
        node = LeafNode("b", text_node.text, None)
        return node
    elif text_node.text_type == TextType.ITALIC_TEXT:
        node = LeafNode("i", text_node.text, None)
        return node
    elif text_node.text_type == TextType.CODE_TEXT:
        node = LeafNode("code", text_node.text, None)
        return node
    elif text_node.text_type == TextType.LINKS:
        convert_props_string_to_dict = {"href": text_node.url}
        node = LeafNode("a", text_node.text, convert_props_string_to_dict)
        return node
    elif text_node.text_type == TextType.IMAGES:
        convert_prop_img_string = {"src": text_node.url, "alt": text_node.text}
        node = LeafNode("img", "", convert_prop_img_string)
        return node
    else:
        raise Exception("Should have text type of NORMAL, BOLD, ITALIC, CODE, LINKS, and IMAGES only")

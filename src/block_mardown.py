from enum import Enum
from split_nodes import text_to_textnodes
from htmlnode import text_node_to_html_node
from textnode import TextNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = []

    split = markdown.split("\n\n")
    for content in split:
        if content.strip():
            blocks.append(content.strip())

    return blocks

    #single block of markdown text input
    #return blockType representing the block
    #all leading and and trailing whitespace are stripped

def block_to_block_type(block):
    split = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in split:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("-"):
        for line in split:
            if not line.startswith("-"):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in split:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

class HTMLNode():
    def __init__(self, tag = None, text = None, children = None):
        self.tag = tag
        self.text = text
        self.children = children or []

    def to_html(self):
        if self.tag is None:
            return self.text or ""
        
        opening_tag = f"<{self.tag}>"

        #if text exist add text
        if self.text:
            opening_tag += self.text

        #recurse to get tags and text
        for child in self.children:
            opening_tag += child.to_html()

        #close tag
        closing_tag = f"</{self.tag}>"
        opening_tag += closing_tag

        return opening_tag
    
def text_to_children(markdown):
    #convert text to list of textnode obj
    text_nodes = text_to_textnodes(markdown)

    html_nodes = []

    #convert text node to html node
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)

    return html_nodes

#Convert to Parent HTML Node
#Parent ccontain many child HTML 
def markdown_to_html_node(markdown):
    #converted markdown in blocks
    split_block = markdown_to_blocks(markdown)
    parent_node = HTMLNode("div", None, [])

    for block in split_block:
        type_of_block = block_to_block_type(block)

        if type_of_block == "paragraph":
            node = HTMLNode("p", None, text_to_children(block))
        elif type_of_block == "heading":
             # Count the number of # characters to determine heading level
            counter = 0
            for char in block:
                if char == '#':
                    counter += 1
                else:
                    break
            # Extract the heading text (removing the # characters and any leading/trailing whitespace)
            heading_text = block[counter:].strip()
            node = HTMLNode(f"h{counter}", None, text_to_children(heading_text))
        elif type_of_block == "code":
            #remove ``` in beg and end with whitespaces
            code_content = block.strip()[3:-3].strip()

            #text node forcode content no inline parsing
            text_node = TextNode(code_content, "text")
            code_node = text_node_to_html_node(text_node)

            node = HTMLNode("pre", None, [code_node])
        elif type_of_block == "quote":
            pass
        elif type_of_block == "unordered_list":
            pass
        elif type_of_block == "ordered_list":
            pass
        parent_node.children.append(node)
    return parent_node
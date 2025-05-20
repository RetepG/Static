from enum import Enum
from split_nodes import text_to_textnodes
from htmlnode import text_node_to_html_node
from textnode import TextNode, TextType

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

        if type_of_block == BlockType.PARAGRAPH:
            paragraph_text = block.replace('\n', ' ')
            node = HTMLNode("p", None, text_to_children(paragraph_text))
        elif type_of_block == BlockType.HEADING:
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
        elif type_of_block == BlockType.CODE:
            # Split the block into lines
            lines = block.strip().split("\n")
    
            # Extract the content lines (skip first and last which have the ```)
            content_lines = lines[1:-1]
    
            # Join with newlines and add an extra newline at the end
            code_content = "\n".join(content_lines) + "\n"
    
            # Create text node with code type
            text_node = TextNode(code_content, TextType.CODE_TEXT)
            code_node = text_node_to_html_node(text_node)
    
            node = HTMLNode("pre", None, [code_node])
        elif type_of_block == BlockType.QUOTE:
            # Remove the '> ' prefix from each line
            quote_lines = block.split('\n')
            clean_lines = []
            for line in quote_lines:
                if line.startswith('>'):
                    # Remove the '>' and any single space after it
                    clean_line = line[1:].lstrip()
                    clean_lines.append(clean_line)
                else:
                    clean_lines.append(line)
    
            quote_content = '\n'.join(clean_lines).strip()
            node = HTMLNode("blockquote", None, text_to_children(quote_content))
        elif type_of_block == BlockType.UNORDERED_LIST:
            # Split the block into list items
            items = block.split('\n')
            list_items = []
    
            for item in items:
                # Remove the '* ' or '- ' prefix and create a list item node
                if item.strip():  # Check if line is not empty
                    # Remove the bullet point and whitespace
                    item_text = item.strip()
                    if item_text.startswith('* ') or item_text.startswith('- '):
                        item_text = item_text[2:]
            
                    # Create the list item node
                    item_node = HTMLNode("li", None, text_to_children(item_text))
                    list_items.append(item_node)
    
             # Create the unordered list node with all list item nodes as children
            node = HTMLNode("ul", None, list_items)
        elif type_of_block == BlockType.ORDERED_LIST:
            # Split the block into list items
            items = block.split('\n')
            list_items = []
    
            for item in items:
                if item.strip():  # Check if line is not empty
                     # Extract the item text by removing the number and dot
                    item_text = item.strip()
                    # Looking for patterns like "1. ", "2. ", etc.
                    for i in range(len(item_text)):
                        if item_text[i] == '.' and i < len(item_text) - 1 and item_text[i+1] == ' ':
                            item_text = item_text[i+2:]  # Skip the number, dot and space
                            break
            
                    # Create the list item node
                    item_node = HTMLNode("li", None, text_to_children(item_text))
                    list_items.append(item_node)
    
            # Create the ordered list node with all list item nodes as children
            node = HTMLNode("ol", None, list_items)
        parent_node.children.append(node)
    return parent_node
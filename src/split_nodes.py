import re
from textnode import *

#Used to convert TextNode class and splitting them depending on delimiter(Bold,Italic, so on)
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    combine_text = []
    for node in old_nodes:
        if node.text_type is not TextType.NORMAL_TEXT:
            combine_text.append(node)
            continue

        split = node.text.split(delimiter)

        if len(split) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        
        for i in range(len(split)):
            parts = split[i]

            if parts:
                if i % 2 == 0:
                    combine_text.append(TextNode(parts, TextType.NORMAL_TEXT))
                else:
                    combine_text.append(TextNode(parts, text_type))

    return combine_text

#Used to find all instances matching images and links in markdown
def extract_markdown_images(text):
    convert_alt_url = re.findall(r'!\[([^\]]+)\]\(([^)]+)\)', text)
    return convert_alt_url

def extract_markdown_links(text):
    convert_anchor_url = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text)
    return convert_anchor_url

#Used to split Images, dividing between text and image
def split_nodes_image(old_nodes):
    combine_text = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            combine_text.append(node)
            continue

        original_text = node.text
        images = extract_markdown_images(original_text)

        if not images:
            combine_text.append(node)
            continue

        for alt_text, url in images:
            split = original_text.split(f"![{alt_text}]({url})", 1)

            if len(split) != 2:
                raise ValueError("Invalid markdown: image section not closed")

            if split[0]:
                combine_text.append(TextNode(split[0], TextType.NORMAL_TEXT))

            combine_text.append(TextNode(alt_text, TextType.IMAGES, url))
            original_text = split[1]

        if split[1]:
            combine_text.append(TextNode(original_text, TextType.NORMAL_TEXT))

    return combine_text

def split_nodes_link(old_nodes):
    comnbine_text = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            comnbine_text.append(node)
            continue
    
        original_text = node.text
        links = extract_markdown_links(original_text)

        if not links:
            comnbine_text.append(node)
            continue

        for alt_text, url in links:
            split = original_text.split(f"[{alt_text}]({url})", 1)

            if len(split) != 2:
                raise ValueError("Invalid markdown: image section not closed")
            
            if split[0]:
                comnbine_text.append(TextNode(split[0], TextType.NORMAL_TEXT))

            comnbine_text.append(TextNode(alt_text, TextType.LINKS, url))
            original_text = split[1]
        
        if split[1]:
            comnbine_text.append(TextNode(original_text, TextType.NORMAL_TEXT))
    return comnbine_text

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL_TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
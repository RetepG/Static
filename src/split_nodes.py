import re
from textnode import *

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

def extract_markdown_images(text):
    convert_alt_url = re.findall(r'!\[([^\]]+)\]\(([^)]+)\)', text)
    return convert_alt_url

def extract_markdown_links(text):
    convert_anchor_url = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text)
    return convert_anchor_url
import re
from textnode import TextNode, TextType





def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
	    
            if len(split_text) % 2 == 0:
                    raise Exception("invalid Markdown syntax")



            for i in range(len(split_text)):
                if split_text[i] == "":
                    continue
                if i % 2 == 0:
                    new_node = TextNode(split_text[i], TextType.TEXT)
                    new_nodes.append(new_node)
                else:
                    new_node = TextNode(split_text[i], text_type)
                    new_nodes.append(new_node)
                

    return new_nodes



def extract_markdown_images(text):

    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):

    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)

        else:
            images = extract_markdown_images(node.text)

            if not images:
                new_nodes.append(node)
                continue
    
            remainder = node.text
            for alt, url in images:
                token = f"![{alt}]({url})"
                before, after = remainder.split(token, 1)
 
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                remainder = after

            if remainder:
                new_nodes.append(TextNode(remainder, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        
        links = extract_markdown_links(node.text)

        if not links:
            new_nodes.append(node)
            continue

        remainder = node.text
        for text, url in links:
            token = f"[{text}]({url})"
            before, after = remainder.split(token, 1)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            remainder = after

        if remainder:
            new_nodes.append(TextNode(remainder, TextType.TEXT))


    return new_nodes

import re

from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError("Invalid Markdown: missing closing delimiter")

        for i in range(len(parts)):
            if parts[i] == "":
                continue

            if i % 2 == 0:
                new_node = TextNode(parts[i], TextType.TEXT)
                new_nodes.append(new_node)
            else:
                new_node = TextNode(parts[i], text_type)
                new_nodes.append(new_node)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        matches = extract_markdown_images(remaining_text)

        if len(matches) == 0:
            new_nodes.append(node)
            continue

        for image_alt, image_url in matches:
            sections = remaining_text.split(f"![{image_alt}]({image_url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            remaining_text = sections[1]

        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        matches = extract_markdown_links(remaining_text)

        if matches == 0:
            new_nodes.append(node)
            continue

        for alt_text, link_url in matches:
            sections = remaining_text.split(f"[{alt_text}]({link_url})")

            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(alt_text, TextType.LINK, link_url))
            remaining_text = sections[1]

        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes_after_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes_after_italic = split_nodes_delimiter(nodes_after_bold, "_", TextType.ITALIC)
    nodes_after_code = split_nodes_delimiter(nodes_after_italic, "`", TextType.CODE)
    nodes_after_image = split_nodes_image(nodes_after_code)
    nodes_after_link = split_nodes_link(nodes_after_image)
    return nodes_after_link


def markdown_to_blocks(markdown):
    markdown_split = markdown.split("\n\n")
    blocks = []

    for i in markdown_split:
        i = i.strip()
        if not i:
            continue
        blocks.append(i)
    return blocks

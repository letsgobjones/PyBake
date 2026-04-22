import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    markdown_split = markdown.split("\n\n")
    blocks = []

    for i in markdown_split:
        i = i.strip()
        if not i:
            continue
        blocks.append(i)
    return blocks


def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if block.startswith("1. "):
        i = 1
        is_ordered_list = True
        for line in lines:
            if not line.startswith(f"{i}. "):
                is_ordered_list = False
                break
            i += 1
        if is_ordered_list:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

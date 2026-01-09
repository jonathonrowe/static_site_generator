from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered list"
    ORDERED = "ordered list"


def every_line_starts_with(text, prefix):
    lines = text.strip().split("\n")
    return all(line and line.startswith(prefix) for line in lines)

def every_line_starts_with_number(text):
    boolean = True
    lines = text.strip().split("\n")
    for i in range(len(lines)):
        if not lines[i].startswith(f"{i+1}. "):
            boolean = False
    return boolean

def block_to_block_type(markdown):
    if markdown.startswith("> "):
        if every_line_starts_with(markdown, "> "):
            return BlockType.QUOTE
        else:
            return BlockType.PARAGRAPH
    if markdown.startswith("- "):
        if every_line_starts_with(markdown, "- "):
            return BlockType.UNORDERED
        else:
            return BlockType.PARAGRAPH
    if markdown.startswith("1. "):
        if every_line_starts_with_number(markdown):
            return BlockType.ORDERED
        else:
            return BlockType.PARAGRAPH
    elif markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif markdown.startswith("```\n") and markdown.endswith("```"):
        return BlockType.CODE
    else:
        return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    markdown = markdown.strip()
    blocks = markdown.split("\n\n")
    for block in blocks:
        block = block.strip()
        if block == "/n" or block == "":
            blocks.remove(block)

    return blocks
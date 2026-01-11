from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered list"
    ORDERED = "ordered list"


def every_line_starts_with(markdown, prefix):
    lines = markdown.split("\n")
    for line in lines:
        if not line.strip():
            continue
        if line == ">":
            continue
        if not line.lstrip().startswith(prefix):
            return False
    return True

def every_line_starts_with_number(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if not line.strip():
            continue
        if not re.match(r"\s*\d+\.", line):
            return False
    return True

def block_to_block_type(markdown):
    lines = markdown.split("\n")
    non_empty = [l for l in lines if l.strip() != ""]
    if not non_empty:
        return BlockType.PARAGRAPH
    first = non_empty[0].lstrip()

    if first.startswith("> "):
        if every_line_starts_with(markdown, "> "):
            return BlockType.QUOTE
        else:
            return BlockType.PARAGRAPH
        
    if first.startswith("- "):
        if every_line_starts_with(markdown, "- "):
            return BlockType.UNORDERED
        else:
            return BlockType.PARAGRAPH
        
    if re.match(r"\d+\. ", first):
        if every_line_starts_with_number(markdown):
            return BlockType.ORDERED
        else:
            return BlockType.PARAGRAPH
        
    elif first.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    elif markdown.startswith("```\n") and markdown.endswith("```"):
        return BlockType.CODE
    
    else:
        return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = []
    current_block_lines = []
    markdown = markdown.strip()
    lines = markdown.split("\n")
    for line in lines:
        if line.strip() == "":
            if current_block_lines:
                blocks.append("\n".join(current_block_lines))
                current_block_lines = []
        else:
            current_block_lines.append(line)
        
    if current_block_lines:
        blocks.append("\n".join(current_block_lines))

    return blocks
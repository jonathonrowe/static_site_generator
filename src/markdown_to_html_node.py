from markdown_to_blocks import *
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for tn in text_nodes:
        children.append(text_node_to_html_node(tn))
    return children

def block_type_to_HTMLNode(block_type, block):
    if block_type == BlockType.PARAGRAPH:
        normalized = block.replace("\n", " ")
        children = text_to_children(normalized)
        return ParentNode("p", children)
    
    elif block_type == BlockType.HEADING:
        if block.startswith("# "):
            text = block[2:]
            children = text_to_children(text)
            return ParentNode("h1", children)
        elif block.startswith("## "):
            text = block[3:]
            children = text_to_children(text)
            return ParentNode("h2", children)
        elif block.startswith("### "):
            text = block[4:]
            children = text_to_children(text)
            return ParentNode("h3", children)
        elif block.startswith("#### "):
            text = block[5:]
            children = text_to_children(text)
            return ParentNode("h4", children)
        elif block.startswith("##### "):
            text = block[6:]
            children = text_to_children(text)
            return ParentNode("h5", children)
        elif block.startswith("###### "):
            text = block[7:]
            children = text_to_children(text)
            return ParentNode("h6", children)
        
    elif block_type == BlockType.CODE:
        lines = block.split("\n")
        inner_lines = lines[1:-1]
        code_text = "\n".join(inner_lines) + "\n"
        code_child = LeafNode(None, code_text)
        code_node = ParentNode("code", [code_child])
        pre_node = ParentNode("pre", [code_node])
        return pre_node
    
    elif block_type == BlockType.QUOTE:
        lines = block.split("\n")
        stripped_lines = []
        for line in lines:
            if line.startswith("> "):
                stripped_lines.append(line[2:])
            else:
                stripped_lines.append(line)
        text = "\n".join(stripped_lines)
        children = text_to_children(text)
        return ParentNode("blockquote", children)
    
    elif block_type == BlockType.UNORDERED:
        children = []
        lines = block.split("\n")
        for line in lines:
            if line.startswith("- "):
                item_text = line[2:]
                li_children = text_to_children(item_text)
                item_node = ParentNode("li", li_children)
                children.append(item_node)
        return ParentNode("ul", children)
    
    elif block_type == BlockType.ORDERED:
        children = []
        lines = block.split("\n")
        for line in lines:
            if not line.strip():
                continue
            dot_index = line.find(". ")
            if dot_index == -1:
                continue
            item_text = line[dot_index + 2:]
            li_children = text_to_children(item_text)
            item_node = ParentNode("li", li_children)
            children.append(item_node)
        return ParentNode("ol", children)

def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        node = block_type_to_HTMLNode(block_type, block)
        children.append(node)

    return ParentNode("div", children)
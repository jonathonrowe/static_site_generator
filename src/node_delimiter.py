from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if text_type == TextType.TEXT:
        return old_nodes
    list_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            list_nodes.append(old_node)
        else:
            if old_node.text.count(delimiter) == 0:
                list_nodes.append(old_node)
            elif old_node.text.count(delimiter) % 2 != 0:
                raise Exception("invalid Markdown syntax")
            else:
                split_nodes = old_node.text.split(delimiter)
                for i in range(len(split_nodes)):
                    if i % 2 == 0:
                       new_node = TextNode(split_nodes[i], TextType.TEXT)
                       list_nodes.append(new_node)
                    else:
                        new_node = TextNode(split_nodes[i], text_type)
                        list_nodes.append(new_node) 

    return list_nodes

def split_nodes_image(old_nodes):
    list_nodes = []
    for old_node in old_nodes:
        extraction_list = extract_markdown_images(old_node.text)
        if len(extraction_list) == 0:
            list_nodes.append(old_node)
        else:
            to_split = old_node.text
            for extraction in extraction_list:
                image_alt = extraction[0]
                image_link = extraction[1]
                sections = to_split.split(f"![{image_alt}]({image_link})", 1)
                if sections[0] != "":
                    text_node = TextNode(sections[0], TextType.TEXT)
                    list_nodes.append(text_node)
                image_node = TextNode(image_alt, TextType.IMAGE, image_link)
                list_nodes.append(image_node)
                to_split = sections[1]
            if to_split != "":
                text_node2 = TextNode(to_split, TextType.TEXT)
                list_nodes.append(text_node2)  
    return list_nodes



def split_nodes_link(old_nodes):
    list_nodes = []
    for old_node in old_nodes:
        extraction_list = extract_markdown_links(old_node.text)
        if len(extraction_list) == 0:
            list_nodes.append(old_node)
        else:
            to_split = old_node.text
            for extraction in extraction_list:
                link_text = extraction[0]
                link_url = extraction[1]
                sections = to_split.split(f"[{link_text}]({link_url})", 1)
                if sections[0] != "":
                    text_node = TextNode(sections[0], TextType.TEXT)
                    list_nodes.append(text_node)
                link_node = TextNode(link_text, TextType.LINK, link_url)
                list_nodes.append(link_node)
                to_split = sections[1]
            if to_split != "":
                text_node2 = TextNode(to_split, TextType.TEXT)
                list_nodes.append(text_node2)  
    return list_nodes
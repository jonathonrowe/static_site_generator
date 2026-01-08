from textnode import TextNode, TextType

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
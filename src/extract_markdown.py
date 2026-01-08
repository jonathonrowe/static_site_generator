import re

def extract_markdown_images(text):
    tup_list = []
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    for match in matches:
        tup = (match[0], match[1])
        tup_list.append(tup)
    return tup_list

def extract_markdown_links(text):
    tup_list = []
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    for match in matches:
        tup = (match[0], match[1])
        tup_list.append(tup)
    return tup_list
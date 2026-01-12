import os
from markdown_to_html_node import markdown_to_html_node
from htmlnode import *
from extract_title import extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as from_file:
        from_md = from_file.read()
    
    with open(template_path, "r") as template_file:
        template = template_file.read()

    html_node = markdown_to_html_node(from_md)
    html_string = html_node.to_html()
    title = extract_title(from_md)
    new_html = template.replace("{{ Title }}", title)
    new_html = new_html.replace("{{ Content }}", html_string)

    try:
        dest_dir = os.path.dirname(dest_path)
        if dest_dir != "":
            os.makedirs(dest_dir, exist_ok=True)
    except OSError as e:
        print(f"Error creating directory {dest_dir}: {e}")

    with open(dest_path, "w") as dest_file:
        dest_file.write(new_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    
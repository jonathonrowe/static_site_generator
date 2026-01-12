import os
from pathlib import Path
from markdown_to_html_node import markdown_to_html_node
from htmlnode import *
from extract_title import extract_title

def markdown_to_html_string(markdown, template):
    html_node = markdown_to_html_node(markdown)
    html_string = html_node.to_html()
    title = extract_title(markdown)
    new_html = template.replace("{{ Title }}", title)
    return new_html.replace("{{ Content }}", html_string)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as from_file:
        from_md = from_file.read()
    
    with open(template_path, "r") as template_file:
        template = template_file.read()

    new_html = markdown_to_html_string(from_md, template)

    try:
        dest_dir = os.path.dirname(dest_path)
        if dest_dir != "":
            os.makedirs(dest_dir, exist_ok=True)
    except OSError as e:
        print(f"Error creating directory {dest_dir}: {e}")

    with open(dest_path, "w") as dest_file:
        dest_file.write(new_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Generating pages from {dir_path_content} to {dest_dir_path} using {template_path}")
    with open(template_path, "r") as template_file:
        template = template_file.read()

    entries = os.listdir(dir_path_content)
    for entry in entries:
        full_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(full_path):
            with open(full_path, "r") as entry_file:
                entry_md = entry_file.read()
            new_html = markdown_to_html_string(entry_md, template)
            
            try:
                os.makedirs(dest_dir_path, exist_ok=True)
            except OSError as e:
                print(f"Error creating directory {dest_dir_path}: {e}")
            
            base_name = os.path.basename(full_path)
            md_file_path = Path(base_name)
            html_name = md_file_path.with_suffix(".html")
            final_path = os.path.join(dest_dir_path, html_name)
            with open(final_path, "w") as dest_file:
                dest_file.write(new_html)
        else:
            dest_full_path = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(full_path, template_path, dest_full_path)
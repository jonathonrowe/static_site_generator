import sys
from textnode import TextNode
from copy_contents import copy_contents
from generate_page import generate_page, generate_pages_recursive

def main():
    copy_contents("static", "docs")
    
    content_path = "content"
    template_path = "template.html"
    dest_dir_path = "docs"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    generate_pages_recursive(content_path, template_path, dest_dir_path, basepath)

if __name__ == "__main__":
    main()
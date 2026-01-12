import sys
from textnode import TextNode
from copy_contents import copy_contents
from generate_page import generate_page, generate_pages_recursive

def main():
    copy_contents("static", "public")

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    generate_pages_recursive("content", "template.html", "public", basepath)

if __name__ == "__main__":
    main()
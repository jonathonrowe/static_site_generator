from textnode import TextNode
from copy_contents import copy_contents
from generate_page import generate_page

def main():
    copy_contents("static", "public")

    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()
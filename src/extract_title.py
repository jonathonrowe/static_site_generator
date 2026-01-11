def extract_title(markdown):
    lines = markdown.strip().split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
def extract_title(markdown):
    lines = markdown.strip().split("\n")
    for line in lines:
        if not line.startswith("# "):
            raise Exception("No h1 header in file")
        elif line.startswith("# "):
            return line[2:]
import os
from markdown2html import markdown_to_html_node

def extract_title(markdown):
    if markdown[:2] != "# ":
        raise Exception("Expected document to start with '# '")
    first_line = markdown.split("\n")[0]
    return first_line[2:]

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    with open(from_path) as markdown_file:
        markdown = markdown_file.read()

    template = ""
    with open(template_path) as template_file:
        template = template_file.read()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html_page = template.replace("{{ Title }}", title)
    html_page = html_page.replace("{{ Content }}", content)

    dest_directory = os.path.dirname(dest_path)
    os.makedirs(dest_directory, exist_ok=True)

    with open(dest_path, "w") as dest_file:
        dest_file.write(html_page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    ls = os.listdir(dir_path_content)
    for filename in ls:
        src = os.path.join(dir_path_content, filename)
        dest = os.path.join(dest_dir_path, filename.replace(".md", ".html"))
        if os.path.isfile(src):
            print(f"Generating html from {src} at {dest}")
            generate_page(src, template_path, dest)
        elif os.path.isdir(src):
            print(f"Creating directory: {dest}")
            os.mkdir(dest)
            generate_pages_recursive(src, template_path, dest)
import os
from src.markdown_blocks import markdown_to_html_node
from pathlib import Path

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return  line[1:].strip()
    raise ValueError("No h1 title found")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page = (
        template
        .replace("{{ Title }}", title)
        .replace("{{ Content }}", html)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )


    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page)



def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath, root=None):
    if root is None:
        root = dir_path_content
    for name in os.listdir(dir_path_content):
        src = os.path.join(dir_path_content, name)
        if os.path.isdir(src):
            generate_pages_recursive(src, template_path, dest_dir_path, basepath, root)
        elif os.path.isfile(src) and src.endswith(".md"):
            
            relpath = Path(src).relative_to(Path(root)) 
            rel_html = relpath.with_suffix(".html")
            dest_path = Path(dest_dir_path) / rel_html
            generate_page(src, template_path, str(dest_path), basepath) 

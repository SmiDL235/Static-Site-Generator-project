import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import shutil
from src.copystatic import copy_static
from src.gencontent import generate_page

def rm_public(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def main():
    rm_public("public")
    copy_static("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()



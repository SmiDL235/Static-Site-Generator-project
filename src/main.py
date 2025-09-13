import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import shutil
from src.copystatic import copy_static
from src.gencontent import generate_pages_recursive

def rm_public(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    rm_public("docs")
    copy_static("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()



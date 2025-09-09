from enum import Enum 
from inline_markdown import text_to_textnodes
from textnode_to_htmlnode import text_node_to_html_node
from htmlnode import ParentNode, LeafNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def _is_ordered_list(block: str) -> bool:
    lines = block.splitlines()
    for i, line in enumerate(lines):
        if not line.startswith(f"{i+1}. "):
            return False
    return True


def _is_unordered_list(block: str) -> bool:
    lines = block.splitlines()
    if not lines:
        return False
    for line in lines:
        if not line.startswith("- "):
            return False
    return True


def _is_quote(block: str) -> bool:
    lines = block.splitlines()
    if not lines:
        return False
    for line in lines:
        if not line.startswith(">"):
            return False
    return True

def _is_heading(block: str) -> bool:
    first = block.splitlines()[0] if block else ""
    if not first:
        return False

    i = 0
    while i < len(first) and first[i] == '#':
        i += 1
    if i == 0 or i > 6:
        return False
    return i < len(first) and first[i] == ' '

def _is_code(block: str) -> bool:
    return block.startswith("```") and block.endswith("```")



def block_to_block_type(block: str) -> BlockType:
    if _is_code(block):
        return BlockType.CODE
    if _is_heading(block):
        return BlockType.HEADING
    if _is_ordered_list(block):
        return BlockType.ORDERED_LIST
    if _is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    if _is_quote(block):
        return BlockType.QUOTE
    return BlockType.PARAGRAPH 





def markdown_to_blocks(markdown:str):
    clean = markdown.strip()
    if not clean:
        return []
    parts = clean.split("\n\n")
    blocks = [p.strip() for p in parts if p.strip()]
    return blocks



def text_to_children(text):
    return [text_node_to_html_node(n) for n in text_to_textnodes(text)]



def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        bt = block_to_block_type(block)
        node = build_block_node(block, bt)
        children.append(node)
    return ParentNode("div", children)


def build_block_node(block, bt):
    if bt == BlockType.CODE:
        lines = block.splitlines()
        inner = "\n".join(lines[1:-1])
        if not inner.endswith("\n"):
            inner += "\n"
        return ParentNode("pre", [ParentNode("code", [LeafNode(None, inner)])])
    if bt == BlockType.PARAGRAPH:
        text = " ".join(block.splitlines())
        return ParentNode("p", text_to_children(text))
    if bt == BlockType.HEADING:
        first = block.splitlines()[0]
        level = len(first) - len(first.lstrip("#"))
        text = first[level+1:]
        return ParentNode(f"h{level}", text_to_children(text))
    if bt == BlockType.QUOTE:
        lines = [l[2:] if l.startswith("> ") else l[1:] for l in block.splitlines()]
        text = " ".join(lines)
        return ParentNode("blockquote", text_to_children(text))
    if bt == BlockType.UNORDERED_LIST:
        items = [l[2:] for l in block.splitlines()]
        li_nodes = [ParentNode("li", text_to_children(it.strip())) for it in items]
        return ParentNode("ul", li_nodes)
    if bt == BlockType.ORDERED_LIST:
        lines = block.splitlines()
        items = [line.split(". ", 1)[1] for line in lines]
        li_nodes = [ParentNode("li", text_to_children(it.strip())) for it in items]
        return ParentNode("ol", li_nodes)
    return ParentNode("p", text_to_children(" ".join(block.splitlines())))

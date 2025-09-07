from enum import Enum 


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

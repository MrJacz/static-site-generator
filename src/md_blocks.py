from enum import Enum

from htmlnode import ParentNode
from inline_md import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

# Enum for different block-level markdown elements
class BlockType(Enum):
    PARAGRAPH = "paragraph"    # Regular paragraphs
    HEADING = "heading"        # # Headers
    CODE = "code"              # ```code blocks```
    QUOTE = "quote"            # > blockquotes
    OLIST = "ordered_list"     # 1. numbered lists
    ULIST = "unordered_list"   # - bullet lists


# Split markdown into logical blocks separated by blank lines
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()  # Remove leading/trailing whitespace
        filtered_blocks.append(block)
    return filtered_blocks


# Determine what type of markdown block we're dealing with
def block_to_block_type(block):
    lines = block.split("\n")

    # Check for headings (1-6 # characters)
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    # Code blocks start and end with ```
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    # Blockquotes - every line must start with >
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    # Unordered lists - every line must start with -
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    # Ordered lists - lines must be numbered sequentially (1. 2. 3. etc.)
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    # Default to paragraph if no other patterns match
    return BlockType.PARAGRAPH


# Main function: convert full markdown document to HTML node tree
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    # Wrap all blocks in a div container
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


# Convert text with inline markdown to list of HTML child nodes
# This handles formatting like **bold**, *italic*, `code`, [links](url), etc.
def text_to_children(text):
    text_nodes = text_to_textnodes(text)  # Parse inline markdown
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)  # Convert to HTML
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

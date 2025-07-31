from htmlnode import LeafNode
from enum import Enum

# Enum for different types of inline text formatting in markdown
class TextType(Enum):
    TEXT = "text"     # Plain text
    BOLD = "bold"     # **bold** or __bold__
    ITALIC = "italic" # *italic* or _italic_
    CODE = "code"     # `code`
    LINK = "link"     # [text](url)
    IMAGE = "image"   # ![alt](url)


# Intermediate representation of text with formatting before conversion to HTML
# This separation allows us to process markdown syntax first, then convert to HTML
class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text           # The actual text content
        self.text_type = text_type # TextType enum value
        self.url = url            # URL for links and images (optional)

    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


# Convert TextNode to HTMLNode - this is where markdown syntax becomes HTML tags
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        # Plain text has no HTML tag wrapper
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        # Links need href attribute from the URL
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        # Images are self-closing, so empty text content
        # Alt text goes in alt attribute, not as content
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"invalid text type: {text_node.text_type}")

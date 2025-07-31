# Base class for HTML element representation using the Composite pattern
# This allows us to treat individual elements and collections uniformly
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag          # HTML tag name (e.g., "p", "div", "a")
        self.value = value      # Text content for leaf nodes
        self.children = children # List of child HTMLNodes for parent nodes
        self.props = props      # Dictionary of HTML attributes

    def to_html(self):
        # Subclasses must implement their own HTML generation logic
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        # Convert props dictionary to HTML attribute string
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


# Leaf nodes represent HTML elements with no children (text, images, etc.)
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        # Leaf nodes never have children, so we pass None explicitly
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        # Raw text nodes have no tag (e.g., plain text inside a paragraph)
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


# Parent nodes represent HTML elements that contain other elements (divs, paragraphs, etc.)
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        # Parent nodes never have direct text value, so we pass None
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        # Recursively generate HTML for all child nodes
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

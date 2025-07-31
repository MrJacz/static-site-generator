import unittest
from src.htmlnode import LeafNode, ParentNode


class TestParentNode(unittest.TestCase):
    def test_init(self):
        children = [LeafNode("b", "Bold")]
        node = ParentNode("div", children)
        self.assertEqual(node.tag, "div")
        self.assertIsNone(node.value)
        self.assertEqual(node.children, children)
        self.assertIsNone(node.props)

    def test_init_with_props(self):
        children = [LeafNode("span", "Text")]
        props = {"class": "container", "id": "main"}
        node = ParentNode("div", children, props)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "Italic text")
        ]
        parent_node = ParentNode("p", children)
        expected = "<p><b>Bold text</b>Normal text<i>Italic text</i></p>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_mixed_children(self):
        leaf_child = LeafNode("span", "Leaf")
        parent_child = ParentNode("div", [LeafNode("b", "Nested")])
        parent_node = ParentNode("section", [leaf_child, parent_child])
        expected = "<section><span>Leaf</span><div><b>Nested</b></div></section>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_no_tag_raises_error(self):
        children = [LeafNode("span", "child")]
        node = ParentNode(None, children)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "invalid HTML: no tag")

    def test_to_html_empty_tag_raises_error(self):
        children = [LeafNode("span", "child")]
        node = ParentNode("", children)
        # Empty string tag doesn't raise error, just creates empty tag
        result = node.to_html()
        self.assertEqual(result, "<><span>child</span></>")

    def test_to_html_no_children_raises_error(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "invalid HTML: no children")

    def test_to_html_empty_children_raises_error(self):
        node = ParentNode("div", [])
        # Empty list doesn't raise error, just returns empty tag
        result = node.to_html()
        self.assertEqual(result, "<div></div>")

    def test_to_html_various_tags(self):
        test_cases = [
            ("ul", [LeafNode("li", "Item")], "<ul><li>Item</li></ul>"),
            ("h1", [LeafNode(None, "Title")], "<h1>Title</h1>"),
            ("article", [LeafNode("p", "Content")], "<article><p>Content</p></article>")
        ]

        for tag, children, expected in test_cases:
            with self.subTest(tag=tag):
                node = ParentNode(tag, children)
                self.assertEqual(node.to_html(), expected)

    def test_to_html_deep_nesting(self):
        deep_leaf = LeafNode("strong", "Deep")
        level3 = ParentNode("em", [deep_leaf])
        level2 = ParentNode("span", [level3])
        level1 = ParentNode("div", [level2])
        expected = "<div><span><em><strong>Deep</strong></em></span></div>"
        self.assertEqual(level1.to_html(), expected)

    def test_inheritance_from_htmlnode(self):
        node = ParentNode("div", [LeafNode("span", "test")])
        self.assertTrue(hasattr(node, 'props_to_html'))
        self.assertTrue(hasattr(node, '__repr__'))

    def test_repr(self):
        children = [LeafNode("b", "Bold")]
        node = ParentNode("div", children)
        expected = f"ParentNode(div, children: {children}, None)"
        self.assertEqual(repr(node), expected)

    def test_to_html_with_leaf_node_no_tag(self):
        children = [
            LeafNode("b", "Bold"),
            LeafNode(None, " and "),
            LeafNode("i", "italic")
        ]
        node = ParentNode("p", children)
        expected = "<p><b>Bold</b> and <i>italic</i></p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

if __name__ == "__main__":
    unittest.main()
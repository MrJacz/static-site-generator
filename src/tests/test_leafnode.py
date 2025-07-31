import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_init(self):
        node = LeafNode("p", "Hello world")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello world")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_props(self):
        props = {"class": "text", "id": "main"}
        node = LeafNode("p", "Hello", props)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.props, props)

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_to_html_with_tag(self):
        node = LeafNode("p", "Hello world")
        self.assertEqual(node.to_html(), "<p>Hello world</p>")

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me")
        node.props = {"href": "https://example.com", "class": "link"}
        result = node.to_html()
        self.assertTrue(result.startswith("<a "))
        self.assertTrue("href=\"https://example.com\"" in result)
        self.assertTrue("class=\"link\"" in result)
        self.assertTrue(result.endswith(">Click me</a>"))

    def test_to_html_empty_value_raises_error(self):
        node = LeafNode("p", "")
        # Empty string doesn't raise error, just creates empty element
        result = node.to_html()
        self.assertEqual(result, "<p></p>")

    def test_to_html_none_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_various_tags(self):
        test_cases = [
            ("h1", "Title", "<h1>Title</h1>"),
            ("span", "Text", "<span>Text</span>"),
            ("div", "Content", "<div>Content</div>"),
            ("b", "Bold", "<b>Bold</b>"),
            ("i", "Italic", "<i>Italic</i>")
        ]

        for tag, value, expected in test_cases:
            with self.subTest(tag=tag):
                node = LeafNode(tag, value)
                self.assertEqual(node.to_html(), expected)

    def test_inheritance_from_htmlnode(self):
        node = LeafNode("p", "Test")
        self.assertTrue(hasattr(node, 'props_to_html'))
        self.assertTrue(hasattr(node, '__repr__'))

    def test_repr(self):
        node = LeafNode("p", "Hello")
        expected = "LeafNode(p, Hello, None)"
        self.assertEqual(repr(node), expected)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

if __name__ == "__main__":
    unittest.main()
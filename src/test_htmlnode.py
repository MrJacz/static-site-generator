import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_init_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_init_with_values(self):
        node = HTMLNode("div", "Hello", ["child1", "child2"], {"class": "test"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_to_html_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self):
        node = HTMLNode(props={"class": "test"})
        node.props = {"class": "test"}
        self.assertEqual(node.props_to_html(), "class=test ")

    def test_props_to_html_multiple(self):
        node = HTMLNode()
        node.props = {"class": "test", "id": "main", "style": "color:red"}
        result = node.props_to_html()
        self.assertIn("class=test ", result)
        self.assertIn("id=main ", result)
        self.assertIn("style=color:red ", result)

    def test_repr(self):
        node = HTMLNode("div", "Hello", [], {"class": "test"})
        expected = "HTMLNode(div, Hello, [], {})"
        self.assertEqual(repr(node), expected)


if __name__ == "__main__":
    unittest.main()
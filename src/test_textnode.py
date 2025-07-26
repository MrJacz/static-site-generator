import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_different_text(self):
        node1 = TextNode("Text 1", TextType.BOLD)
        node2 = TextNode("Text 2", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_eq_different_text_type(self):
        node1 = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_eq_different_url(self):
        node1 = TextNode("Text", TextType.LINK, "url1")
        node2 = TextNode("Text", TextType.LINK, "url2")
        self.assertNotEqual(node1, node2)

    def test_eq_with_url(self):
        node1 = TextNode("Link text", TextType.LINK, "https://example.com")
        node2 = TextNode("Link text", TextType.LINK, "https://example.com")
        self.assertEqual(node1, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "url")
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node.url, "url")
        self.assertEqual(node2.url, None)

    def test_init_all_text_types(self):
        text_types = [TextType.TEXT, TextType.BOLD, TextType.ITALIC, 
                     TextType.CODEBLOCK, TextType.LINK, TextType.IMAGE]
        
        for text_type in text_types:
            node = TextNode("Test text", text_type)
            self.assertEqual(node.text, "Test text")
            self.assertEqual(node.text_type, text_type)
            self.assertIsNone(node.url)

    def test_init_with_url(self):
        node = TextNode("Link text", TextType.LINK, "https://example.com")
        self.assertEqual(node.text, "Link text")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.url, "https://example.com")

    def test_repr(self):
        node = TextNode("Test text", TextType.BOLD, "test_url")
        expected = "TextNode(Test text, TextType.BOLD, test_url)"
        self.assertEqual(repr(node), expected)

    def test_repr_no_url(self):
        node = TextNode("Test text", TextType.ITALIC)
        expected = "TextNode(Test text, TextType.ITALIC, None)"
        self.assertEqual(repr(node), expected)

    def test_text_type_values(self):
        self.assertEqual(TextType.TEXT.value, "text")
        self.assertEqual(TextType.BOLD.value, "**")
        self.assertEqual(TextType.ITALIC.value, "_")
        self.assertEqual(TextType.CODEBLOCK.value, "`")
        self.assertEqual(TextType.LINK.value, "[]()")
        self.assertEqual(TextType.IMAGE.value, "![]()")


if __name__ == "__main__":
    unittest.main()
import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_url(self):
        url1 = TextNode("This is url node", TextType.LINKS, None)
        url2 = TextNode("This is url node", TextType.LINKS, None)
        self.assertEqual(url1, url2)

    def test_text(self):
        diff = TextNode("This is a text node", TextType.BOLD_TEXT)
        diff2 = TextNode("This is a text node", TextType.NORMAL_TEXT)
        self.assertNotEqual(diff, diff2)

    def test_not_text(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        node2 = TextNode("This is a text node2", TextType.NORMAL_TEXT)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC_TEXT, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT, "https://www.boot1.dev")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
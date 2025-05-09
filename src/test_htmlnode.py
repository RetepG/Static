import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_no_props(self):
        node = HTMLNode("p", "Hello", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_tag(self):
        node = HTMLNode("Hello", "World", None, None)
        self.assertEqual(node.tag, "Hello")
    
    def test_props_to_html_with_one_prop(self):
        node = HTMLNode("a", "Click me", None, {"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_tag(self):
        node = LeafNode(None, "Click me", {"href": "https://example.com"})
        self.assertEqual(node.tag, None)

    def test_string(self):
        node = LeafNode("p", "Click me", {"href": "https://example.com"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Click me")
        self.assertEqual(node.props, {"href": "https://example.com"})
        
        props_html = node.props_to_html()
        self.assertTrue(' href="https://example.com"' in props_html)

    # Add more test cases for leaf node
    # A regular tag with value renders correctly
    # A node with no tag renders just the text value
    # A node with no value raises a ValueError
    # A node with properties renders those correctly in the tag
    
    def test_props_to_html_with_multiple_props(self):
        node = HTMLNode("a", "Click me", None, {
            "href": "https://example.com",
            "target": "_blank"
        })
        # Since dictionaries don't guarantee order, we need to check if both properties
        # are in the string, regardless of order
        props_html = node.props_to_html()
        self.assertTrue(' href="https://example.com"' in props_html)
        self.assertTrue(' target="_blank"' in props_html)
        # Verify there's exactly one space at the beginning of each attribute
        self.assertEqual(props_html.count(' '), 2)
        # Verify the total length is correct (accounting for both attributes)
        expected_length = len(' href="https://example.com"') + len(' target="_blank"')
        self.assertEqual(len(props_html), expected_length)

    def test_htmlnode_with_children(self):
    # Create child nodes
        child1 = HTMLNode("span", "This is ", None, None)
        child2 = HTMLNode("b", "bold", None, None)
        child3 = HTMLNode("span", " text", None, None)
    
    # Create parent node with children
        parent = HTMLNode("p", None, [child1, child2, child3], {"class": "paragraph"})
    
    # Test that the children are correctly assigned
        self.assertEqual(len(parent.children), 3)
        self.assertEqual(parent.children[0], child1)
        self.assertEqual(parent.children[1], child2)
        self.assertEqual(parent.children[2], child3)
    
    # Test the props_to_html method
        self.assertEqual(parent.props_to_html(), ' class="paragraph"')

if __name__ == "__main__":
    unittest.main()
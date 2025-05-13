import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    #--------------------------------Test for htmlnode
    def test_props_to_html_with_no_props(self):
        node = HTMLNode("p", "Hello", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_tag(self):
        node = HTMLNode("Hello", "World", None, None)
        self.assertEqual(node.tag, "Hello")
    
    def test_props_to_html_with_one_prop(self):
        node = HTMLNode("a", "Click me", None, {"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

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

    #------------------------------------Test Leaf Node
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

    def test_notag(self):
        node = LeafNode(None, "Click me", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), "Click me")

    def test_novalue(self):
        node = node = LeafNode("p", None, {"href": "https://example.com"})
        with self.assertRaises(ValueError):
            node.to_html()

    #--------------------------------------Test Parent Node

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_with_multiple_children(self):
        child1 = LeafNode("b", "bold text")
        child2 = LeafNode(None, "normal text")
        child3 = LeafNode("i", "italic text")
        parent = ParentNode("p", [child1, child2, child3])
        self.assertEqual(
            parent.to_html(),
            "<p><b>bold text</b>normal text<i>italic text</i></p>"
        )

    def test_parentnode_children(self):
        child1 = ParentNode("b", None)
        with self.assertRaises(ValueError):
            child1.to_html()

    def test_parentnode_tag(self):
        child1 = LeafNode("b", "bold text")
        child2 = LeafNode(None, "normal text")
        node = ParentNode(None, [child1, child2])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_empty_children(self):
        node = ParentNode("p", [])
        self.assertEqual(node.to_html(), "<p></p>")

    def test_parent_children(self):
        child1 = LeafNode("b", "bold text")
        child2 = LeafNode(None, "normal text")
        child3 = LeafNode("i", "italic text")
        child4 = LeafNode("b", "italic text")
        parent = ParentNode("p", [child1, child2, child3])
        parent2 = ParentNode("p", [child4, parent])
        self.assertEqual(
            parent2.to_html(),
            "<p><b>italic text</b><p><b>bold text</b>normal text<i>italic text</i></p></p>"
        )

    #-----------------------------Test text_node_to_html
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGES, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

if __name__ == "__main__":
    unittest.main()
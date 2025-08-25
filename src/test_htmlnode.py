import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestMyFunction(unittest.TestCase):

    def test_no_props(self):
        node = HTMLNode()
        noProps = node.props_to_html()

        self.assertEqual(noProps, "")

    def test_one_prop(self):
        node2 = HTMLNode(props={"href": "https://www.boot.dev"})

        oneProp = node2.props_to_html()

        self.assertEqual(oneProp, ' href="https://www.boot.dev"')

    def test_multiple_props(self):

        node3 = HTMLNode(props={ 
        "href": "https://www.google.com",
        "target": "_blank",
        })

        multiProp = node3.props_to_html()

        self.assertEqual(multiProp, ' href="https://www.google.com" target="_blank"')


    def test_repr__(self):
        node = HTMLNode()
        repr = node.__repr__()

        self.assertEqual(repr, 'HTMLNode: tag = None value = None children = None props = None') 


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">Click me!</a>')

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Just text!")
        self.assertEqual(node.to_html(), "Just text!")

    def test_leaf_raises_without_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()


class TestParentNode(unittest.TestCase):

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



if __name__ == "__main__":
    unittest.main()

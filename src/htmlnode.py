class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError 

    def props_to_html(self):
        if not self.props:
            return ""
        propList = []
        for key in self.props:
            propList.append(f'{key}="{self.props[key]}"')

        return " "+" ".join(propList)


    def __repr__(self):
        return f'HTMLNode: tag = {self.tag} value = {self.value} children = {self.children} props = {self.props}' 


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):

        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError

        if not self.tag:
            return f"{self.value}"

        props_str = ""
        if self.props:
            prop_pairs = []
            for key, value in self.props.items():
                prop_pairs.append(f'{key}="{value}"')
            props_str = " " + " ".join(prop_pairs)

        return f'<{self.tag}{props_str}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):

        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):

        if not self.tag:
            raise ValueError

        if not self.children:
            raise ValueError("node has no children")

        children_str = ""
        for child in self.children:
            child_str = child.to_html()
            children_str = children_str + child_str

        return f'<{self.tag}{self.props_to_html()}>{children_str}</{self.tag}>' 


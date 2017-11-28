class Node(object):
    def __init__(self, block, **properties):
        for key, value in properties.items():
            setattr(self, key, value)

        self.block = block
        self.id = None
        self.connector = None

    def can_connect(self, node):
        return (node is not self) and (node.block is not self.block)


class Input(Node):
    def can_connect(self, node):
        return not isinstance(node, Input) and super(Input, self).can_connect(node)


class Output(Node):
    def can_connect(self, node):
        return not isinstance(node, Output) and super(Output, self).can_connect(node)
class Node:
    TYPE = 'Node'

    def __init__(self, block, id=None, **properties):
        for key, value in properties.items():
            setattr(self, key, value)

        self.block = block
        self.id = id
        self.connector = None

    def disconnect(self):
        if self.connector:
            self.connector.disconnect()

    def can_connect(self, node):
        return (node is not self) and (node.block is not self.block) and not self.connector and not node.connector


class Input(Node):
    TYPE = 'Input'

    def can_connect(self, node):
        return not isinstance(node, Input) and super(Input, self).can_connect(node)


class Output(Node):
    TYPE = 'Output'

    def can_connect(self, node):
        return not isinstance(node, Output) and super(Output, self).can_connect(node)
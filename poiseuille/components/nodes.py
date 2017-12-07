from .connector import Connector

class Node(object):
    def __init__(self, block, **properties):
        for key, value in properties.items():
            setattr(self, key, value)

        self.block = block
        self.id = None
        self.connector = None

    def connect(self, node):
        if self.can_connect(node):
            self.disconnect()
            node.disconnect()
            self.connector = Connector()
            self.connector.connect(self, node)
            return self.connector

    def disconnect(self):
        if self.connector:
            self.connector.disconnect()

    def can_connect(self, node):
        return (node is not self) and (node.block is not self.block) and not self.connector and not node.connector


class Input(Node):
    def can_connect(self, node):
        return not isinstance(node, Input) and super(Input, self).can_connect(node)


class Output(Node):
    def can_connect(self, node):
        return not isinstance(node, Output) and super(Output, self).can_connect(node)

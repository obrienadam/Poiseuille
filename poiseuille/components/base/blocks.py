from poiseuille.equation import Term, Equation

class Block:
    def __init__(self, name='Block'):
        self.name = name
        self.nodes = []

    def add_nodes(self, *nodes):
        self.nodes.extend(nodes)

    def continuity_equation(self):
        conn_resistances = [node.connector.r for node in self.nodes]
        conn_nodes = [node.connector.other(node) for node in self.nodes]

        return Equation(
            [Term(node, 1. / r) for node, r in zip(conn_nodes, conn_resistances)]
            + [Term(node, -1. / r) for node, r in zip(self.nodes, conn_resistances)],
            rhs=0.
        )

    def disconnect(self):
        for node in self.nodes:
            node.disconnect()

    def type(self):
        return 'Block'

    def properties(self):
        raise NotImplementedError('Update properties not implemented for block type "{}".'.format(self.type()))

    def solution(self):
        raise NotImplementedError('Update properties not implemented for block type "{}".'.format(self.type()))

    def equations(self):
        raise NotImplementedError('Update properties not implemented for block type "{}".'.format(self.type()))

    def update_properties(self, **kwargs):
        raise NotImplementedError('Update properties not implemented for block type "{}".'.format(self.type()))

    def update_solution(self, **kwargs):
        raise NotImplementedError('Update solution is not implemented for block type "{}".'.format(self.type()))

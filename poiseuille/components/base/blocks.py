from poiseuille.equation import Term, Equation


class Block:
    TYPE = 'Block'
    UNITS = {}

    def __init__(self, name='Block', id=None):
        self.name = name
        self.id = id
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

    def properties(self):
        raise NotImplementedError

    def property_ranges(self):
        raise NotImplementedError

    def solution(self):
        raise NotImplementedError

    def equations(self):
        raise NotImplementedError

    def update_properties(self, **kwargs):
        raise NotImplementedError

    def update_solution(self, **kwargs):
        raise NotImplementedError

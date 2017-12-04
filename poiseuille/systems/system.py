import scipy.sparse as sp
import scipy.sparse.linalg as spla
import numpy as np

class System(object):
    def __init__(self, blocks=[]):
        self.blocks = blocks

    def assign_node_ids(self):
        for id, node in enumerate(self.nodes()):
            node.id = id

    def nodes(self):
        return [node for block in self.blocks for node in block.nodes]

    def connectors(self):
        connectors = []
        for node in self.nodes():
            if not node.connector in connectors:
                connectors.append(node.connector)
        return connectors

    def equations(self):
        return [eqn for block in self.blocks for eqn in block.equations()]

    def linear_system(self):
        self.assign_node_ids()
        eqns = self.equations()
        rows = [row for id, eqn in enumerate(eqns) for row in [id] * len(eqn.terms)]
        cols = [term.node.id for eqn in eqns for term in eqn.terms]
        vals = [term.coeff for eqn in eqns for term in eqn.terms]

        return sp.coo_matrix((vals, (rows, cols)), shape=(len(eqns),) * 2).tocsr(), np.array([eqn.rhs for eqn in eqns])

    def map_solution_to_nodes(self, soln):
        raise NotImplementedError

    def solve(self):
        raise NotImplementedError


class IncompressibleSystem(System):
    def map_solution_to_nodes(self, soln):
        for id, node in enumerate(self.nodes()):
            node.p = soln[id]

    def solve(self, max_iters=10, toler=1e-10):
        x = None

        for iter in range(max_iters):
            A, rhs = self.linear_system()

            if x is not None:
                if np.linalg.norm(A*x - rhs) <= toler:
                    break

            x = spla.spsolve(A, rhs)
            self.map_solution_to_nodes(x)

            for connector in self.connectors():
                connector.update_properties()
                connector.update_solution()

            for block in self.blocks:
                block.update_solution()

        return iter, np.linalg.norm(A*x - rhs)


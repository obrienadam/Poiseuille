import scipy.sparse as sp
import scipy.sparse.linalg as spla
import scipy.optimize as opt
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

        for conn in self.connectors():
            conn.update_solution()

        for block in self.blocks:
            block.update_solution()

    def solve(self, max_iters=10, toler=1e-10):
        def M(x):
            A, rhs = self.linear_system()
            return spla.spsolve(A, x)

        def residual(x):
            self.map_solution_to_nodes(x)
            A, rhs = self.linear_system()
            return A*x - rhs

        p = np.array([node.p for node in self.nodes()])
        p = opt.newton_krylov(residual, p, verbose=1, inner_M=spla.LinearOperator((p.shape[0], p.shape[0]), M), f_tol=1e-10)

        self.map_solution_to_nodes(p)

        return iter
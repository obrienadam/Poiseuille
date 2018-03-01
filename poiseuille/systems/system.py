from enum import Enum

import scipy.sparse as sp
import scipy.sparse.linalg as spla
import scipy.optimize as opt
from scipy.optimize.nonlin import NoConvergence
import numpy as np


class Status(Enum):
    UNSOLVED = 0
    SOLVED = 1
    INVALID_SYSTEM_STATE = 2
    NO_CONVERGENCE = 3
    NAN_DETECTED = 4


class System:
    def __init__(self, blocks=[]):
        self.blocks = blocks
        self.status = Status.UNSOLVED
        self.assign_node_ids()

    def nodes(self):
        return [node for block in self.blocks for node in block.nodes]

    def get_unconnected_nodes(self):
        return [node for node in self.nodes() if not node.connector]

    def assign_node_ids(self):
        ids = []
        for id, node in enumerate(self.nodes()):
            ids.append(id)
            node.id = id

        return ids

    def connectors(self):
        return set((node.connector for node in self.nodes()))

    def equations(self):
        return (eqn for block in self.blocks for eqn in block.equations())

    def compute_matrix(self):
        eqns = tuple(self.equations())
        rows = [row for id, eqn in enumerate(eqns) for row in [id] * len(eqn.terms)]
        cols = [term.node.id for eqn in eqns for term in eqn.terms]
        vals = [term.coeff for eqn in eqns for term in eqn.terms]
        return sp.coo_matrix((vals, (rows, cols)), shape=(len(eqns),) * 2).tocsr()

    def compute_rhs(self):
        return np.array([eqn.rhs for eqn in self.equations()])

    def compute_linear_system(self):
        self.assign_node_ids()
        eqns = tuple(self.equations())
        rows = [row for id, eqn in enumerate(eqns) for row in [id] * len(eqn.terms)]
        cols = [term.node.id for eqn in eqns for term in eqn.terms]
        vals = [term.coeff for eqn in eqns for term in eqn.terms]

        return sp.coo_matrix((vals, (rows, cols)), shape=(len(eqns),)*2).tocsr(), np.array([eqn.rhs for eqn in eqns])

    def map_solution_to_nodes(self, soln):
        raise NotImplementedError

    def solve(self, maxiter=2000, toler=1e-10, verbose=0, method='lgmres'):
        raise NotImplementedError

    class LinearPreconditioner(spla.LinearOperator):
        def __init__(self, num_nodes, system):
            super().__init__(shape=(num_nodes, num_nodes), dtype=np.float64)
            self.system = system

        def _matvec(self, x):
            return spla.spsolve(self.system.matrix, x)

        def _matmat(self, X):
            return spla.spsolve(self.system.matrix, X)

class IncompressibleSystem(System):
    def map_solution_to_nodes(self, soln):
        for node in self.nodes():
            node.p = soln[node.id]

        for conn in self.connectors():
            conn.update_solution()

        for block in self.blocks:
            block.update_solution()

    def residual(self, p):
        self.map_solution_to_nodes(p)
        self.matrix, self.rhs = self.compute_linear_system()
        return self.matrix * p - self.rhs

    def solve(self, maxiter=2000, toler=1e-10, verbose=0, method='lgmres'):
        if self.get_unconnected_nodes():
            self.status = Status.INVALID_SYSTEM_STATE
            return

        x0 = np.array([node.p for node in self.nodes()])
        self.map_solution_to_nodes(x0)

        inner_M = IncompressibleSystem.LinearPreconditioner(len(self.nodes()), self)

        try:
            p = opt.newton_krylov(self.residual,
                                  x0,
                                  verbose=verbose,
                                  inner_M=inner_M,
                                  f_tol=toler,
                                  method=method,
                                  maxiter=maxiter,
                                  inner_maxiter=1,
                                  outer_k=3)
        except NoConvergence as e:  # If iterations fail, restart using zeros
            try:
                x0 = np.zeros(len(self.nodes()))
                self.map_solution_to_nodes(x0)

                p = opt.newton_krylov(self.residual,
                                      x0,
                                      verbose=verbose,
                                      inner_M=inner_M,
                                      f_tol=toler,
                                      method=method,
                                      maxiter=maxiter)
            except NoConvergence as e:
                self.status = Status.NO_CONVERGENCE
                return
        except ValueError as e:
            self.status = Status.NAN_DETECTED
            self.map_solution_to_nodes(np.zeros(len(self.nodes())))
            return

        self.status = Status.SOLVED
        self.map_solution_to_nodes(p)

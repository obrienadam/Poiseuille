from enum import Enum

import numpy as np
import scipy.optimize as opt


class Objectives(Enum):
    MINIMIZE_SUM_ABS = 0
    MINIMIZE_SUM_SQR = 1


class Constraints(Enum):
    GREATER_THAN = 0
    LESS_THAN = 1
    EQUAL_TO = 2


class Optimizer:
    def __init__(self, system=None, ):
        self.system = system

        self.objective_type = Objectives.MINIMIZE_SUM_SQR

        self.objective_blocks = []

        self.constraints = {
            constraint: [] for constraint in Constraints
        }

    def add_objective_block(self, block, attr):
        if block in self.system.blocks:
            self.objective_blocks.append((block, attr))

    def add_constraint(self, type, value, block, attr):
        if block in self.system.blocks:
            self.constraints[type].append((block, value, attr))

    def clear(self):
        self.objective_blocks.clear()
        for val in self.constraints.values():
            val.clear()

    def callback(self, x):
        pass

    def obj_func(self, x):
        if self.objective_type == Objectives.MINIMIZE_SUM_SQR:
            return np.sum(x[:len(self.objective_blocks)] ** 2)
        elif self.objective_type == Objectives.MINIMIZE_SUM_ABS:
            return np.sum(np.abs(x[:len(self.objective_blocks)]))

    def get_constraint_funcs(self):
        constraints = []

        for type, blocks in self.constraints.items():
            for block, value, attr in self.constraints[type]:
                if type == Constraints.EQUAL_TO:
                    constraints.append({
                        'type': 'eq',
                        'fun': lambda x: getattr(block, attr) - value
                    })
                elif type == Constraints.LESS_THAN:
                    constraints.append({
                        'type': 'ineq',
                        'fun': lambda x: value - getattr(block, attr)
                    })
                elif type == Constraints.GREATER_THAN:
                    constraints.append({
                        'type': 'ineq',
                        'fun': lambda x: getattr(block, attr) - value
                    })


    def optimize(self, toler=1e-6):
        initial = self.get_initial_guess()
        constraints = self.get_constraints()
        obj_func = self.get_obj_func()

        opt.minimize(self.obj_func, self.get_initial_guess(), constraints=self.constraints, tol=toler)

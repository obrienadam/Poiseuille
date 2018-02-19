from enum import Enum
import itertools

import numpy as np
import scipy.optimize as opt


class Objectives(Enum):
    MINIMIZE_SUM_ABS = 0
    MINIMIZE_SUM_SQR = 1


class ObjectiveFunction:
    def __init__(self, blocks, var, callback, type=Objectives.MINIMIZE_SUM_SQR):
        self.blocks = blocks
        self.var = var
        self.callback = callback

        if type == Objectives.MINIMIZE_SUM_SQR:
            self.func = lambda: sum(getattr(block, self.var) ** 1 for block in self.blocks)
        elif type == Objectives.MINIMIZE_SUM_ABS:
            self.func = lambda: sum(abs(getattr(block, self.var)) for block in self.blocks)

    def __call__(self, vals):
        self.callback(vals, resolve=False)
        return self.func()


class ConstraintFunction:
    def __init__(self, block, var, type, value, callback, dependent=True):
        self.block = block
        self.var = var
        self.type = type
        self.value = value
        self.callback = callback
        self.dependent = dependent

    def get_dict(self):
        return {
            'type': self.type,
            'fun': self.__call__
        }

    def __call__(self, vals):
        self.callback(vals, resolve=self.dependent)
        return getattr(self.block, self.var) - self.value


class Optimizer:
    def __init__(self, system):
        self.system = system
        self.independent_vars = []
        self.dependent_vars = []

        self.objective_func = None
        self.constraint_funcs = []

    def clear(self):
        self.independent_vars.clear()
        self.dependent_vars.clear()
        self.objective_func = None
        self.constraint_funcs.clear()

    def callback(self, vals, resolve=True):
        for var, val in zip(self.independent_vars, vals):
            setattr(var[0], var[1], val)

        if resolve:
            self.system.solve(maxiter=2500, toler=1e-10, verbose=1, method='lgmres')

    def init_objective_function(self, blocks, var):
        self.independent_vars.extend((block, var) for block in blocks)
        self.objective_func = ObjectiveFunction(blocks, var, self.callback)

    def init_property_objective_function(self, blocks, property):
        self.init_objective_function(blocks, blocks[0].SYMBOLS[property])

    def add_constraint(self, block, var, type, value, dependent=True):
        if dependent:
            self.dependent_vars.append((block, var))
            self.constraint_funcs.append(ConstraintFunction(block, var, type, value, self.callback, dependent=True))
        else:
            if not (block, var) in set(self.independent_vars):
                self.independent_vars.append((block, var))
            self.constraint_funcs.append(ConstraintFunction(block, var, type, value, self.callback, dependent=False))

    def add_property_constraint(self, block, property, type, value):
        self.add_constraint(block, block.SYMBOLS[property], type, value, False)

    def add_solution_constraint(self, block, solution, type, value):
        self.add_constraint(block, block.SYMBOLS[solution], type, value, True)

    def optimize(self, guess=[], maxiter=1000, verbose=1):
        constr = [c.get_dict() for c in self.constraint_funcs]

        if len(guess) < len(self.independent_vars):
            guess += [0] * (len(self.independent_vars) - len(guess))

        opts = {
            'maxiter': maxiter,
            'disp': bool(verbose)
        }

        opt.minimize(self.objective_func, x0=guess[:len(self.independent_vars)], constraints=constr, options=opts)

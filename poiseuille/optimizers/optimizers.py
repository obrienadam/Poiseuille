import scipy.optimize as opt

class Optimizer:
    class Variable:
        def __init__(self, block, attr, alias=None):
            self.block = block
            self.attr = attr
            self.alias = alias

        @property
        def value(self):
            return getattr(self.block, self.attr)

        @value.setter
        def value(self, value):
            setattr(self.block, self.attr, value)

    def __init__(self, system=None):
        self.system = system
        self.variables = []
        self.constraints = []

        self.variable_map = {}

    def clear(self):
        self.variables.clear()
        self.constraints.clear()
        self.variable_map.clear()

    def add_variable(self, block, property, name):
        if not name in self.variable_map:
            self.variable_map[name] = len(self.variables)
            self.variables.append({
                'name': name,
                'property': property,
                'block': block
            })

    def add_inequality_constraint(self, var, value=0.):
        index = self.variable_map[var]
        if index:
            self.constraints.append({
                'type': 'ineq',
                'func': lambda x: x[index] - value
            })

    def get_variable(self, name):
        return self.variables[name]['value']

    def get_initial_guess(self):
        return [variable['value'] for variable in self.variables]

    def optimize(self, tol=1e-6):
        initial = self.get_initial_guess()
        constraints = self.get_constraints()
        obj_func = self.get_obj_func()

        opt.minimize(self.obj_func, self.get_initial_guess(), constraints=self.constraints, tol=tol)

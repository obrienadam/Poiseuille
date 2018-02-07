class Term(object):
    def __init__(self, node, coeff):
        self.node = node
        self.coeff = coeff

class Equation(object):
    def __init__(self, terms=None, rhs=0.):
        self.terms = terms if terms else []
        self.rhs = rhs

    def add_terms(self, *terms):
        self.terms.extend(terms)
class Term(object):
    def __init__(self, node, coeff):
        self.node = node
        self.coeff = coeff

class Equation(object):
    def __init__(self, terms=[], rhs=0.):
        self.terms = terms
        self.rhs = rhs

    def add_terms(self, *terms):
        self.terms.extend(terms)
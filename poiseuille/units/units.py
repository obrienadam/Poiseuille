import numpy as np


class Unit:
    SYMBOLS = 'L', 'M', 'T', 'Phi'

    def __init__(self, L=0, M=0, T=0, Phi=0):
        self.base = np.array((L, M, T, Phi))  # L, M, T, Phi

    def is_dimensionless(self):
        return not self.base.any()

    def __str__(self):
        num = tuple('{}^{}'.format(b, p) for b, p in zip(self.SYMBOLS, self.base) if p > 0)
        den = tuple('{}^{}'.format(b, abs(p)) for b, p in zip(self.SYMBOLS, self.base) if p < 0)

        if num and den:
            return '{} ({}/{})'.format(self.value, ''.join(num), ''.join(den))
        elif num:
            return '{} ({})'.format(self.value, ''.join(num))
        elif den:
            return '{} ({})'.format(self.value, ''.join(den))
        else:
            return '{}'.format(self.value)

    def __eq__(self, other):
        return self.base == other.base

    def __mul__(self, other):
        return Unit(self.base + other.base)

    def __truediv__(self, other):
        return Unit(self.base - other.base)

    def __pow__(self, power):
        return Unit(power * self.base)


class Pascal(Unit):
    def __init__(self):
        super().__init__()
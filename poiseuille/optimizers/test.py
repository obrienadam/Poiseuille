import scipy.optimize as opt

class f:
    def __init__(self):
        self.i = 0

    def __call__(self, x):
        self.i += 1
        print(self.i)
        return sum([v**2 for v in x])

def g1(x):
    return x[0] - 10

def g2(x):
    return x[1] - 4

def g3(x):
    return abs(x[2] - x[3]) - 5

result = opt.minimize(f(), x0=[.1, .5, .6, .3, .4, 5., 1., .2], constraints=[{'type': 'ineq', 'fun': g1}, {'type': 'ineq', 'fun': g2}, {'type': 'eq', 'fun': g3}])

print(result)
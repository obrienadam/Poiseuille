class Property:
    def __init__(self, name, symbol=None, value=0., min_value=float('-inf'), max_value=float('inf'), units=''):
        self.name = name
        self.symbol = symbol if symbol else self.name.lower()
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.units = units
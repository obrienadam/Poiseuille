class Connector:
    TYPE = 'Connector'

    def __init__(self, name='Connector', id=None):
        self.name = name
        self.id = id
        self.input = None
        self.output = None
        self.constraints = {}

    @property
    def nodes(self):
        return self.input, self.output

    def connect(self, input, output):
        if input.can_connect(output):
            self.disconnect()
            self.input = input
            self.output = output
            input.connector = self
            output.connector = self
            return True
        return False

    def disconnect(self):
        if self.input:
            self.input.connector = None

        if self.output:
            self.output.connector = None

        self.input = None
        self.output = None

    def other(self, node):
        if node is self.input:
            return self.output
        elif node is self.output:
            return self.input
        else:
            raise ValueError('Node is not attached to this connector.')

    def properties(self):
        raise NotImplementedError

    def property_ranges(self):
        raise NotImplementedError

    def property_units(self):
        raise NotImplementedError

    def solution(self):
        raise NotImplementedError

    def solution_units(self):
        raise NotImplementedError

    def update_properties(self, **kwargs):
        raise NotImplementedError

    def update_solution(self):
        raise NotImplementedError

 #!/usr/bin/env python
# -*- coding: utf-8 -*-


class ExecutionPoint:
    '''Class ExecutionPoint:
    This class explains execution point in dtraces
    Execution point is all about method: its class and name,
    its parameters and initial field values
    and also its children – execution points for nested methods.
    '''
    def __init__(self, program_class, method_name, parameters, fields):
        self.program_class = program_class
        self.method_name = method_name
        self.parameters = parameters
        self.fields = fields
        self.nodes = []

    def add_child(self, node):
        self.nodes.append(node)

    def get_condition(self):
        return self.condition

    def get_parameters(self):
        return self.parameters

    def get_name(self):
        return self.name

    def get_children(self):
        return self.nodes

    def add_values(self, values):
        self.values = values

    def get_values(self):
        return self.values

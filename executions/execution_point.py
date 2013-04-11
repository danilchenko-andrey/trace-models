 #!/usr/bin/env python
# -*- coding: utf-8 -*-


class ExecutionPoint:
    '''Class ExecutionPoint:
    This class explains execution point in dtraces
    Execution point is all about method: its class and name,
    its parameters and initial field values
    and also its children – execution points for nested methods.
    '''
    def __init__(self, program_class, method_name, parameters, full_parameters, fields):
        self.program_class = program_class
        self.method_name = method_name
        self.parameters = parameters
        self.full_parameters = full_parameters
        self.fields = fields
        self.conditions = {}
        if len(fields) > 0:
            for field in fields.split(" & "):
                key = field.split("_eq_")[0]
                value = field.split("_eq_")[1]
                self.conditions[key] = value
        self.nodes = []

    def add_child(self, node):
        self.nodes.append(node)

    def get_condition(self):
        return self.fields

    def get_parsed_fields(self):
        return self.conditions

    def get_parameters(self):
        return self.parameters

    def get_full_parameters(self):
        result = ""
        for p in self.full_parameters:
            if len(result) > 0:
                result += ", "
            result += "%s=%s" % (p, self.full_parameters[p])
        return result

    def get_name(self):
        return "%s.%s" % (self.program_class.get_name(), self.method_name)

    def get_children(self):
        return self.nodes

    def add_values(self, values):
        self.values = values

    def get_values(self):
        return self.values

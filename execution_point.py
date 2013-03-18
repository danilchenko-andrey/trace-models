#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ExecutionPoint:

    def __init__(self, name, parameters, condition):
        self.name = name
        self.condition = condition
        self.parameters = parameters
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

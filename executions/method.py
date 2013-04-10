#!/usr/bin/env python
# -*- coding: utf-8 -*-


class MethodMetaInfo:

    def __init__(self, name):
        self.name = name
        self.params = {}
        self.invariant_params = {}
        self.invariant_variable = {}
        self.variables = {}

    def add_possible_param(self, name, value):
        if name not in self.params:
            self.params[name] = set(value)
        else:
            self.params[name].add(value)

    def add_possible_variable(self, name, value):
        if name not in self.variables:
            self.variables[name] = set(value)
        else:
            self.variables[name].add(value)

    def set_invariant_param(self, name, values):
        self.invariant_params[name] = values

    def set_invariant_variable(self, name, values):
        self.invariant_variable[name] = values

    def __eq__(self, other):
        return self.name == other.name and self.params == other.params and self.variables == other.variables

    def __hash__(self):
        result = self.name.__hash__()
        result = 31 * result + self.params.__repr__().__hash__()
        result = 31 * result + self.variables.__repr__().__hash__()
        return result


class MethodCall:

    def __init__(self, meta, params={}, variables={}):
        self.meta = meta
        self.params = {}
        for p in params:
            self.param(p, params[p])
        self.variables = {}
        for v in variables:
            self.variable(v, variables[v])

    def param(self, name, value):
        self.meta.add_possible_param(name, value)
        self.params[name] = value

    def variable(self, name, value):
        self.meta.add_possible_variable(name, value)
        self.variables[name] = value

    def matches(self, params, variables):
        for p in params:
            if self.params[p] != params[p]:
                return False
        for v in variables:
            if self.variables[v] != variables[v]:
                return False
        return True

    def __eq__(self, other):
        return self.meta == other.meta and self.variables == other.variables and self.params == other.params

    def __hash__(self):
        result = self.meta.__hash__()
        result = 31 * result + self.params.__repr__().__hash__()
        result = 31 * result + self.variables.__repr__().__hash__()
        return result

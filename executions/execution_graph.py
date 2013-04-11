#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from method import MethodMetaInfo, MethodCall


class ExecutionNode:

    def __init__(self, name):
        self.method = MethodMetaInfo(name)
        self.edges = {}
        self.merged_edges = {}
        self.terminal = True
        logging.debug("GRAPH: created node %s" % name)

    def name(self):
        return self.method.name

    def add_edge(self, other_node, params, variables):
        self.terminal = False
        this_call = MethodCall(self.method, params, variables)
        if other_node.name() not in self.edges:
            self.edges[other_node.name()] = set()
        self.edges[other_node.name()].add(this_call)

    def get_edges_matching(self, dst, params, variables):
        result = []
        for dst in self.edges:
            for edge in self.edges[dst]:
                if edge.matches(params, variables):
                    result.append(edge)
        return result

    def is_param_significant(self, dst, name):
        if len(self.method.params[name]) < 2:  # too few possible values
            return False
        for dst_edge in self.edges[dst]:
            params = dst_edge.params.copy()
            del params[name]
            for other_dst in set(self.edges.keys()) - set([dst]):
                for other_edge in self.edges[other_dst]:
                    if other_edge.matches(params, dst_edge.variables):
                        return True
        return False

    def get_significant_params(self, dst):
        result = set()
        for v in self.method.params:
            if self.is_param_significant(dst, v):
                result.add(v)
        return result

    def is_variable_significant(self, dst, name):
        if len(self.method.variables[name]) < 2:  # too few possible values
            return False
        for dst_edge in self.edges[dst]:
            variables = dst_edge.variables.copy()
            del variables[name]
            for other_dst in set(self.edges.keys()) - set([dst]):
                for other_edge in self.edges[other_dst]:
                    if other_edge.matches(dst_edge.params, variables):
                        return True
        return False

    def get_significant_variables(self, dst):
        result = set()
        for v in self.method.variables:
            if self.is_variable_significant(dst, v):
                result.add(v)
        return result

    def print_edges(self):
        for dst in self.edges:
            logging.debug("GRAPH: edge %s => %s" % (self.name(), dst))
            variables = ""
            for v in self.get_significant_variables(dst):
                if len(variables) > 0:
                    variables += ", "
                variables += v + " of %s" % sorted(list(self.method.variables[v]))
            logging.debug("GRAPH: important (%s) [%s]" % (", ".join(self.get_significant_params(dst)), variables))


class ExecutionGraph:

    def __init__(self):
        self.root = None
        self.nodes = {}
        self.node_stack = []
        self.current_node = None
        self.current_params = {}
        self.current_variables = {}

    def on_method_enter(self, name, params, variables):
        if name not in self.nodes:
            self.nodes[name] = ExecutionNode(name)
        if not self.root:
            self.root = self.nodes[name]
        if self.current_node:
            self.node_stack.append({"node": self.current_node, "params": self.current_params, "variables": self.current_variables})
            self.current_node.add_edge(self.nodes[name], self.current_params, self.current_variables)
        self.current_node = self.nodes[name]
        self.current_params = params
        self.current_variables = variables

    def on_method_exit(self, name):
        if len(self.node_stack) > 0:
            top = self.node_stack.pop()
            self.current_node = top["node"]
            self.current_params = top["params"]
            self.current_variables = top["variables"]
        else:
            self.current_node = None
            self.current_params = {}
            self.current_variables = {}
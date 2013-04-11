#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import logging

from program_class import ProgramClass
from execution_point import ExecutionPoint

from execution_graph import *


class Program:

    def __init__(self, debug=False):
        self.classes = {}
        self.debug = debug
        self.events = {}
        self.outputs = {}
        self.fields = {}
        self.graph = ExecutionGraph()

    def hello(self):
        logging.debug("Hello from Program class")

    def read_program_points(self, dtrace_filename):
        dtrace_file = open(dtrace_filename, 'rt')
        line = dtrace_file.readline()
        while line:
            m = re.search("^ppt ([^()]*)\.([^:]*):::ENTER", line)
            if m:
                class_name = m.group(1)
                if class_name not in self.classes:
                    self.classes[class_name] = ProgramClass(class_name)
                method_name = m.group(2)
                variables = {}
                variable = None
                line = dtrace_file.readline()

                while len(line) > 0 and not line.startswith("ppt "):
                    m = re.search("^ *variable (.*)", line)
                    if m:
                        if variable and variable["name"] != "this" and variable["type"] == "int":
                            variables[variable["name"]] = variable
                            variables[variable["name"]]["n"] = chr(len(variables) + 96)
                        variable = {"name": m.group(1)}
                        line = dtrace_file.readline()
                        continue
                    var_kind = re.search("^ *var-kind ([^ \n]*)", line)
                    if var_kind:
                        variable["kind"] = var_kind.group(1)
                    dec_type = re.search("^ *dec-type ([^ \n]*)", line)
                    if dec_type:
                        variable["type"] = dec_type.group(1)

                    line = dtrace_file.readline()

                if variable and variable["name"] != "this" and variable["type"] == "int":
                    variables[variable["name"]] = variable
                    variables[variable["name"]]["n"] = chr(len(variables) + 96)

                self.classes[class_name].add_method(method_name, variables)

            else:
                line = dtrace_file.readline()
        dtrace_file.close()

    def update_fields(self):
        for k in self.fields:
            self.fields[k] = set(self.fields[k])

    def get_full_condition(self, condition):
        if len(condition) == 0:
            return ""
        #self.update_fields()
        result = ""
        for c in condition.split(" & "):
            k = c.split("_eq_")[0]
            v = c.split("_eq_")[1]
            for cond in self.fields[k]:
                if len(result) > 0:
                    result += " & "
                if cond != v:
                    result += "!"
                result += "%s_%s" % (k, cond)
        return result

    def read_program_executions(self, dtrace_filename, no_print=False):
        test_scenario_states = []
        test_scenario_outputs = []
        dtrace_file = open(dtrace_filename, 'rt')
        line = dtrace_file.readline()

        stack = []
        # self.events = {}
        # self.outputs = {}

        while line:
            m_enter = re.search("^([^() ]*)\.([^:]*):::ENTER", line)
            if m_enter:
                class_name = m_enter.group(1)
                if class_name not in self.classes:
                    raise RuntimeError("Unknown class %s" % class_name)
                clazz = self.classes[class_name]
                method = m_enter.group(2)

                line = dtrace_file.readline()

                parameters = ""
                condition = ""

                parameter_values = {}
                variable_values = {}
                while len(line.strip()) > 0:
                    if line.strip() in clazz.methods[method]:
                        key = line.strip()
                        value = dtrace_file.readline().strip()
                        if not key.startswith("this."):
                            parameter_values[key] = value
                            if len(parameters) > 0:
                                parameters += " & "
                            parameters += "%s_eq_%s" % (clazz.methods[method][key]["n"], value)
                        else:
                            variable_values[key] = value
                            if len(condition) > 0:
                                condition += " & "
                            condition += "%s_eq_%s" % (clazz.methods[method][key]["n"], value)
                    line = dtrace_file.readline()

                if self.debug:
                    prefix = ""
                    for i in xrange(len(stack)):
                        prefix += "."
                    logging.debug("method called %s%s.%s (%s) [%s]" % (prefix, class_name, method, parameters, condition))
                if no_print:
                    self.graph.on_method_enter("%s.%s" % (class_name, method), parameter_values, variable_values)

                point = ExecutionPoint(clazz, method, parameters, condition)

                for k in point.get_parsed_fields():
                    if k not in self.fields:
                        self.fields[k] = set()
                    self.fields[k].add(point.get_parsed_fields()[k])
                stack.append(point)
                if len(stack) > 1:
                    stack[len(stack) - 2].add_child(point)

                continue

            m_exit = re.search("^([^() ]*)\.([^:]*):::EXIT[0-9]*", line)
            if m_exit:
                class_name = m_exit.group(1)
                if class_name not in self.classes:
                    raise RuntimeError("Unknown class %s" % class_name)
                method = m_exit.group(2)
                if no_print:
                    self.graph.on_method_exit("%s.%s" % (class_name, method))
                line = dtrace_file.readline()

                point = stack.pop()

                if len(stack) == 0:
                    s = [point]

                    while len(s) > 0:
                        p = s.pop()
                        if len(p.get_children()) == 0:
                            continue

                        node = self.graph.nodes[p.get_name()]
                        significant_variables = set()

                        event = p.get_name() + p.get_parameters()
                        if not event in self.events:
                            self.events[event] = "STATE_%s" % chr(65 + len(self.events))
                            if len(self.events) == 91:
                                print >> sys.stderr, "OMG!!!!"
                        output = ""
                        for c in p.get_children():
                            if len(c.get_children()) == 0:
                                significant_variables.update(node.get_significant_variables(c.get_name()))
                                if len(output) > 0:
                                    output += ", "
                                if not c.get_name() in self.outputs:
                                    self.outputs[c.get_name()] = "z%d" % len(self.outputs)
                                output += self.outputs[c.get_name()]
                            else:
                                s.append(c)
                        if len(test_scenario_outputs) > 0:
                            test_scenario_outputs.append(output)
                        else:
                            test_scenario_outputs.append("")

                        test_cond = ""
                        for significant_variable in significant_variables:
                            var_name = p.program_class.methods[p.method_name][significant_variable]["n"]
                            var_value = p.get_parsed_fields()[var_name]
                            for possible_value in self.graph.nodes[p.get_name()].method.variables[significant_variable]:
                                if len(test_cond) > 0:
                                    test_cond += " & "
                                if possible_value == var_value:
                                    test_cond += "%var_s_eq_%s" % (var_name, var_value)
                                else:
                                    test_cond += "!%var_s_eq_%s" % (var_name, possible_value)
                                logging.debug("EVENT DECODE: var_%s_eq_ = %s" % (var_name, significant_variable))
                        if len(test_cond) > 0:
                            test_cond = " [%s]" % test_cond
                        if self.debug:
                            logging.debug("EVENT: %s%s" % (event, test_cond))
                            logging.debug("EVENT DECODE: %s = %s" % (event, self.events[event]))

                        test_scenario_states.append("%s%s" % (self.events[event], test_cond))

                continue

            line = dtrace_file.readline()

        dtrace_file.close()

        if not no_print:
            #output_file = open("scenarios", "a")
            #output_file.write("%s\n" % "; ".join(test_scenario_states))
            #output_file.write("%s\n" % "; ".join(test_scenario_outputs))
            #output_file.close()
            print "; ".join(test_scenario_states)
            print "; ".join(test_scenario_outputs)

            for node in self.graph.nodes.values():
                node.print_edges()

    def get_class(self, name):
        return self.classes[name]

    def read_program_invariants(self, invariants_filename):
        invariants_file = open(invariants_filename, 'rt')
        line = invariants_file.readline()
        while line:
            m_enter = re.search("^([^() ]*)\.([^:]*):::ENTER", line)
            if m_enter:
                class_name = m_enter.group(1)
                if class_name not in self.classes:
                    raise RuntimeError("Unknown class %s" % class_name)
                clazz = self.classes[class_name]
                method = m_enter.group(2)
                #print "Invariants for %s.%s..." % (class_name, method)
                line = invariants_file.readline()
                while not line.startswith("="):
                    m_equal_invariant = re.search("^([^() ]*) == ([0-9]*)$", line)
                    if m_equal_invariant:
                        variable = m_equal_invariant.group(1)
                        value = m_equal_invariant.group(2)
                        #print "%s == %s" % (variable, value)
                        clazz.methods[method][variable]["possible_values"] = [value]
                        #print clazz.get_methods()[method][variable]
                    m_oneof_invariant = re.search("^([^() ]*) one of {(.*)}$", line)
                    if m_oneof_invariant:
                        variable = m_oneof_invariant.group(1)
                        values = m_oneof_invariant.group(2).replace(" ", "").split(",")
                        #print "%s one of %s" % (variable, values)
                        clazz.methods[method][variable]["possible_values"] = values
                        #print clazz.get_methods()[method][variable]
                    line = invariants_file.readline()
            line = invariants_file.readline()

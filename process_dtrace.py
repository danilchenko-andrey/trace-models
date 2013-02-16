#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

from execution_tree import ExecutionPoint


class AutomatonTrace:

    def __init__(self, class_name):
        self.class_name = class_name
        self.methods = {}

    def read_program_points(self, dtrace_filename):

        dtrace_file = open(dtrace_filename, 'rt')
        line = dtrace_file.readline()
        while line:
            m = re.search("^ppt %s.([^:]*):::ENTER" % self.class_name, line)
            if m:
                method_name = m.group(1)
                #print "+ %s" % method_name
                method_variables = {}
                variable = None
                line = dtrace_file.readline()

                while len(line) > 0 and not line.startswith("ppt "):
                    m = re.search("^ *variable (.*)", line)
                    if m:
                        if variable and\
                         variable["name"] != "this" and \
                         variable["type"] == "int":
                            #print "   - %s" % variable["name"]
                            method_variables[variable["name"]] = variable
                            method_variables[variable["name"]]["n"] = chr(len(method_variables) + 96)
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

                if variable and\
                 variable["name"] != "this" and\
                 variable["type"] == "int":
                    #print "   - %s" % variable["name"]
                    method_variables[variable["name"]] = variable
                    method_variables[variable["name"]]["n"] = chr(len(method_variables) + 96)

                #print method_variables
                self.methods[method_name] = method_variables
                self.methods[method_name]["n"] = chr(len(self.methods) + 64)
                self.methods[method_name]["m"] = "z%s" % len(self.methods)
                print >> sys.stderr, "%s => %s; %s" % (method_name, self.methods[method_name]["n"], self.methods[method_name]["m"])

            else:
                line = dtrace_file.readline()
        dtrace_file.close()
        #print "--------------------------"
        #print ""

    def read_program_executions(self, dtrace_filename):
        dtrace_file = open(dtrace_filename, 'rt')
        line = dtrace_file.readline()

        stack = []
        events = {}

        while line:
            m_enter = re.search("^%s.(.*):::ENTER" % self.class_name, line)
            if m_enter:
                method = m_enter.group(1)
                #print " + %s" % method
                line = dtrace_file.readline()

                parameters = ""
                condition = ""
                while len(line.strip()) > 0:
                    if line.strip() in self.methods[method]:
                        key = line.strip()
                        if not key.startswith("this.lastNumberPressed"):
                            value = dtrace_file.readline().strip()
                            if not key.startswith("this."):
                                if len(parameters) > 0:
                                    parameters += " & "
                                parameters += "%s_eq_%s" % (self.methods[method][key]["n"], value)
                            else:
                                if len(condition) > 0:
                                    condition += " & "
                                condition += "%s_eq_%s" % (self.methods[method][key]["n"], value)
                    line = dtrace_file.readline()
                #if parameters:
                #    parameters = " [" + parameters + "]"
                if condition:
                    condition = " [" + condition + "]"

                stack.append(ExecutionPoint(method, parameters, condition))
                if len(stack) > 1:
                    stack[len(stack) - 2].add_child(stack[len(stack) - 1])

                continue
            m_exit = re.search("^%s.(.*):::EXIT.*" % self.class_name, line)
            if m_exit:
                method = m_exit.group(1)
                line = dtrace_file.readline()

                new_values = {}
                while len(line.strip()) > 0:
                    if line.strip() in self.methods[method]:
                        key = line.strip()
                        value = int(dtrace_file.readline().strip())
                        #print "set %s=%d" % (key, value)
                        new_values[key] = value
                    line = dtrace_file.readline()

                execution_point = stack.pop()
                execution_point.add_values(new_values)

                if len(stack) == 0:
                    s = [execution_point]
                    states = []
                    outputs = []
                    while len(s) > 0:
                        p = s.pop()
                        event = p.get_name() + p.get_condition()
                        if not event in events:
                            events[event] = chr(65 + len(events))
                            if len(events) == 91:
                                print >> sys.stderr, "OMG!!!!"
                        cond = p.get_parameters()
                        if cond:
                            cond = " [" + cond + "]"
                        states.append("%s%s" % (events[event], cond))
                        output = ""
                        for c in p.get_children():
                            if len(output) > 0:
                                output += ", "
                            output += self.methods[c.get_name()]["m"] + c.get_parameters()
                            if len(c.get_children()) > 0:
                                s.append(c)
                        #for k, v in p.get_values().iteritems():
                            #if len(output) > 0:
                            #    output += ", "
                            #print k, p.get_name(), self.methods[p.get_name()][k]
                            #output += "%s_eq_%s" % (self.methods[p.get_name()][k]["n"], v)
                        outputs.append(output)
                        #s.extend(p.get_children())
                    print "; ".join(states)
                    print "; ".join(outputs)
                    print ""
                    #print "@@ "

                continue

            line = dtrace_file.readline()

        dtrace_file.close()


if __name__ == '__main__':
    trace = AutomatonTrace(sys.argv[1])
    trace.read_program_points(sys.argv[2])
    trace.read_program_executions(sys.argv[2])

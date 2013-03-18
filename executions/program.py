#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from program_class import ProgramClass


class Program:

    def __init__(self):
        self.classes = {}

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

    def read_program_executions(self, dtrace_filename):
        test_scenario_states = []
        test_scenario_outputs = []
        dtrace_file = open(dtrace_filename, 'rt')
        line = dtrace_file.readline()

        stack = []
        events = {}

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
                l = line.strip()
                while len(l) > 0:
                    if l in clazz.methods[method]:
                        key = line.strip()
                        value = dtrace_file.readline().strip()
                        if not key.startswith("this."):
                            if len(parameters) > 0:
                                parameters += " & "
                            parameters += "%s_eq_%s" % (clazz.methods[method][key]["n"], value)
                        else:
                            if len(condition) > 0:
                                condition += " & "
                            condition += "%s_eq_%s" % (clazz.methods[method][key]["n"], value)
                    line = dtrace_file.readline()
                #if parameters:
                #    parameters = " [" + parameters + "]"
                if condition:
                    condition = " [" + condition + "]"

                stack.append(ExecutionPoint(method, parameters, condition))
                if len(stack) > 1:
                    stack[len(stack) - 2].add_child(stack[len(stack) - 1])

                continue

            m_exit = re.search("^([^() ]*)\.([^:]*):::EXIT.*", line)
            if m_exit:
                class_name = m_enter.group(1)
                if class_name not in self.classes:
                    raise RuntimeError("Unknown class %s" % class_name)
                method = m_exit.group(2)
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

                    while len(s) > 0:
                        p = s.pop()
                        event = p.get_name() + p.get_parameters()
                        if not event in events:
                            events[event] = chr(65 + len(events))
                            if len(events) == 91:
                                print >> sys.stderr, "OMG!!!!"

                        test_scenario_states.append("%s%s" % (events[event], p.get_condition()))
                        output = ""
                        for c in p.get_children():
                            if len(output) > 0:
                                output += ", "
                            output += self.methods[c.get_name()]["m"]
                            if len(c.get_children()) > 0:
                                s.append(c)
                        # for k, v in p.get_values().iteritems():
                        #     if len(output) > 0:
                        #         output += ", "
                        #     # print k, p.get_name(), self.methods[p.get_name()][k]
                        #     output += "%s_eq_%s" % (self.methods[p.get_name()][k]["n"], v)
                        test_scenario_outputs.append(output)
                        # s.extend(p.get_children())
                    # test_scenario_states.append(string.join(states, "; "))
                    #test_scenario_outputs.append(string.join(outputs , "; "))
                    #print "; ".join(states)
                    #print "; ".join(outputs)
                    #print ""
                    #print "@@ "

                continue

            line = dtrace_file.readline()

        dtrace_file.close()

        print "; ".join(test_scenario_states)
        print "; ".join(test_scenario_outputs)

    def get_class(self, name):
        return self.classes[name]

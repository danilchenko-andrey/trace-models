#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys


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

            else:
                line = dtrace_file.readline()
        dtrace_file.close()

    def read_program_executions(self, dtrace_filename):
        dtrace_file = open(dtrace_filename, 'rt')
        line = dtrace_file.readline()

        stack = []
        last_stack_length = 0

        while line:
            m_enter = re.search("^%s.(.*):::ENTER" % self.class_name, line)
            if m_enter:
                method = m_enter.group(1)
                print " + %s" % method
                stack.append(method)
                last_stack_length = len(stack)
                line = dtrace_file.readline()

                condition = ""
                while len(line.strip()) > 0:
                    #print len(line), "%%", line.strip(), "%%"
                    if line.strip() in self.methods[method]:
                        key = line.strip()
                        value = dtrace_file.readline().strip()
                        if len(condition) > 0:
                            condition += " & "
                        condition += "%s_eq_%s" % (self.methods[method][key]["n"], value)
                    line = dtrace_file.readline()
                if condition:
                    condition = " [" + condition + "]"
                print "@@ %s;" % (self.methods[method]["m"])
                print "@@ "
                print "@@ %s%s;" % (self.methods[method]["n"], condition)

                continue
            m_exit = re.search("^%s.(.*):::EXIT.*" % self.class_name, line)
            if m_exit:
                method = m_exit.group(1)

                if len(stack) == last_stack_length:
                    print " * %s" % method
                stack.pop()
                #last_stack_length = len(stack)
                print " - %s" % method

                line = dtrace_file.readline()

                new_values = {}
                while len(line.strip()) > 0:
                    #print len(line), "%%", line.strip(), "%%"
                    if line.strip() in self.methods[method]:
                        key = line.strip()
                        value = int(dtrace_file.readline().strip())
                        print "set %s=%d" % (key, value)
                        new_values[key] = value
                    line = dtrace_file.readline()

                if len(stack) == 0:
                    print "================="
                    #print "@@ "

                continue

            line = dtrace_file.readline()

        dtrace_file.close()


if __name__ == '__main__':
    trace = AutomatonTrace(sys.argv[1])
    trace.read_program_points(sys.argv[2])
    trace.read_program_executions(sys.argv[2])

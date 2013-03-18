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
            m = re.search("^ppt (.*).([^:]*):::ENTER", line)
            if m:
                class_name = m.group(1)
                if not self.classes[class_name]:
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

                variables["n"] = chr(len(self.methods) + 64)
                variables["m"] = "z%s" % len(self.methods)
                self.classes[class_name].add_method(method_name, variables)

            else:
                line = dtrace_file.readline()
        dtrace_file.close()

    def get_class(self, name):
        return self.classes[name]

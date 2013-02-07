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
                print "+ %s" % method_name
                method_variables = {}
                variable = None
                line = dtrace_file.readline()

                while len(line) > 0 and not line.startswith("ppt "):
                    m = re.search("^ *variable (.*)", line)
                    if m:
                        if variable and\
                         variable["name"] != "this" and \
                         variable["type"] == "int":
                            print "   - %s" % variable["name"]
                            method_variables[variable["name"]] = variable
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
                    print "   - %s" % variable["name"]
                    method_variables[variable["name"]] = variable

                #print method_variables
                self.methods[method_name] = method_variables

            else:
                line = dtrace_file.readline()
        dtrace_file.close()


if __name__ == '__main__':
    AutomatonTrace(sys.argv[1]).read_program_points(sys.argv[2])

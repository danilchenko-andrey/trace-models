#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ProgramClass:
    '''Class ProgramClass:
    This class store some meta-information about single class: its name,
    methods (simply maps now).
    Fields are not supported because of source of this meta-information, we can
    only know them and their values in runtime with execution poits.
    '''
    def __init__(self, name):
        self.name = name
        self.methods = {}

    def get_name(self):
        return self.name

    def get_methods(self):
        return self.methods

    def add_method(self, name, method):
        self.methods[name] = method

    def __str__(self):
        result = "%s {" % self.name
        for k in self.methods:
            result += "\n + %s" % k
        result += "\n}"
        return result

    def __repr__(self):
        return self.__str__()

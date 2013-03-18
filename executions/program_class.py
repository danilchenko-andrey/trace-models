#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ProgramClass:

    def __init__(self, name):
        self.name = name
        self.methods = {}

    def get_name(self):
        return self.name

    def get_methods(self):
        return self.methods

    def add_method(self, name, method):
        self.methods[name] = method

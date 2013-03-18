#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from executions import *


if __name__ == '__main__':
    program = Program()
    program.read_program_points(sys.argv[1])
    for c in program.classes:
        print program.get_class(c)
    program.read_program_executions(sys.argv[1])

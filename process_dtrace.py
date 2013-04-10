#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from executions import *


if __name__ == '__main__':
    program = Program()
    program.read_program_points("%s.0" % sys.argv[2])
    #program.read_program_invariants("%s.invariants" % sys.argv[2])
    #program.debug = True
    #for i in xrange(int(sys.argv[1])):
    #    program.read_program_executions("%s.%d" % (sys.argv[2], i), True)

    for i in xrange(int(sys.argv[1])):
        program.read_program_executions("%s.%d" % (sys.argv[2], i))

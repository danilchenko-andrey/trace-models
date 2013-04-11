#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging

from executions import Program


def main():
    program_name = sys.argv[2]
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s", filename="process-dtrace.log", filemode='w')
    logging.debug("Starting work with %s" % program_name)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("%(message)s")
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    program = Program()
    program.debug = True
    program.read_program_points("%s.0" % program_name)
    #program.read_program_invariants("%s.invariants" % program_name)
    for i in xrange(int(sys.argv[1])):
        program.read_program_executions("%s.%d" % (program_name, i), True)

    for i in xrange(int(sys.argv[1])):
        program.read_program_executions("%s.%d" % (program_name, i))

    logging.debug("Finished work with %s" % program_name)

if __name__ == '__main__':
    main()

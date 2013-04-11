#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging

from executions import *


if __name__ == '__main__':
    program_name = sys.argv[2]
    logger = logging.getLogger("default")
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler("%s.log" % program_name)
    fh.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter("%(filename)s:%(lineno)d %(asctime)s [%(levelname)s] %(message)s")
    fh.setFormatter(file_formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    console_formatter = logging.Formatter("%(asctime)s %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    program = Program()
    program.read_program_points("%s.0" % program_name)
    #program.read_program_invariants("%s.invariants" % program_name)
    program.debug = True
    for i in xrange(int(sys.argv[1])):
        program.read_program_executions("%s.%d" % (program_name, i), True)

    for i in xrange(int(sys.argv[1])):
        program.read_program_executions("%s.%d" % (program_name, i))

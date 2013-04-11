#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys


def main():
    key_file = open(sys.argv[1], 'r')
    events = {}
    pattern = re.compile("^(STATE_[A-Z]*) = (.*)$")
    for line in key_file:
        key_line = re.search(pattern, line.strip())
        if key_line:
            events[key_line.group(1)] = key_line.group(2)
    key_file.close()

    for line in sys.stdin:
        print re.sub("(STATE_[A-Z]*)", lambda m: events[m.group(1)], line),


if __name__ == "__main__":
    main()

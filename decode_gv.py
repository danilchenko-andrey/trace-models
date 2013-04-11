#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


def main():
    key_file = open(sys.argv[1], 'r')
    events = {}
    for line in key_file:
        parts = line.strip().split(" = ")
        events[parts[0]] = parts[1]
    key_file.close()

    for line in sys.stdin:
        s = line
        for e in events:
            s = s.replace(e, events[e])
        print s,


if __name__ == "__main__":
    main()

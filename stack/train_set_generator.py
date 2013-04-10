#!/usr/bin/env python

import random
import sys


def main():
    steps = random.randint(1, int(sys.argv[1]))
    for s in xrange(steps):
        step = random.randint(1, 3)
        if step == 1:
            print 'a',
        if step == 2:
            print 'r',
        if step == 3:
            print 's',

if __name__ == '__main__':
    main()

#!/usr/bin/env python

import random
import sys


def main():
    steps = random.randint(1, int(sys.argv[1]))
    for s in xrange(steps):
        step = random.randint(1, 10)
        if step == 1:
            print 'h',
        if step == 2:
            print 'm',
        if step == 3:
            print 'a',
        if step >= 4:
            print 't',
    print 'q'

if __name__ == '__main__':
    main()

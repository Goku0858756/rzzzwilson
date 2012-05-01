#!/usr/bin/env python

"""
Program to make a test dataset.

Usage: make_dataset.py <file> <N>
"""

import sys
import random


MaxN = 10000000
MaxHeight = 100000000
MaxWidth = 1000


if len(sys.argv) != 3:
    print __doc__
    sys.exit(10)

filename = sys.argv[1]
N = int(sys.argv[2])

if N >= MaxN:
    print("N can't be %d or greater.\n" % MaxN)
    print __doc__
    sys.exit(10)

with open(filename, 'w') as fd:
    fd.write('%d\n' % N)
    for _ in xrange(N):
        width = random.randint(1, MaxWidth-1)
        height = random.randint(1, MaxHeight-1)
        fd.write('%d %d ' % (width, height))
    fd.write('\n')
fd.close()

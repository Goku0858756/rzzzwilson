#!/usr/bin/env python

"""
A program to solve the Google All Your Base puzzle.

Usage:  base.py <datafile>
"""


def solve_puzzle():
    """Solve the puzzle.

    Returns the 
    """

    result = 1
    return result
        
def main(N, fd):
    """Solve the puzzle.

    N   is the number of datasets
    fd  is the open file to read datasets from
    """

    for case in xrange(N):
        result = solve_puzzle()
        print('Case #%d: %d' % (case+1, result))

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print __doc__
        sys.exit(10)

    buildings = []
    fd = open(sys.argv[1], 'r')
    N = int(fd.readline())

    main(N, fd)

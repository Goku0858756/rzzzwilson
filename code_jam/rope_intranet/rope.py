#!/usr/bin/env python

"""
A program to solve the Google Rope Intraner puzzle.

Usage:  rope.py <datafile>
"""


def read_dataset(fd):
    """Read one dataset from 'fd'.

    Return (T, <pair_list>) where <pair_list> is a list of
    2-tuples defining left and right windows.
    """

    T = int(fd.readline())
    pair_list = []
    for _ in xrange(T):
        line = fd.readline()
        (left, right) = line.split()
        pair_list.append((int(left), int(right)))
    return (T, pair_list)

def solve_puzzle(pair_list):
    """Solve the puzzle.

    pair_list  list of (left, right) window tuples

    Returns the number of intersections.
    """

    result = 0

    # sort pair_list by left window, low to high
    pair_list.sort()

    while len(pair_list) > 1:
        (ll, lr) = pair_list[0]
        for (hl, hr) in pair_list[1:]:
            if hr < lr:
                result += 1
        pair_list = pair_list[1:]

    return result
        
def main(N, fd):
    """Solve the puzzle.

    N   is the number of datasets
    fd  is the open file to read datasets from
    """

    for case in xrange(N):
        (T, pair_list) = read_dataset(fd)
        num_intersect = solve_puzzle(pair_list)
        print('Case #%d: %d' % (case+1, num_intersect))

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print __doc__
        sys.exit(10)

    buildings = []
    fd = open(sys.argv[1], 'r')
    N = int(fd.readline())

    main(N, fd)

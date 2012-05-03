#!/usr/bin/env python

"""
A program to solve the Google All Your Base puzzle.

Usage:  base.py <datafile>
"""

import itertools


# maximum result value
MaxResult = 10 ** 18

# maximum base allowed (as only 36 symbols)
MaxBase = 36

# minimum base allowed (from problem definition)
# not sure we need this
MinBase = 2

# all allowable values
AllValues = None


def solve_puzzle(line):
    """Solve the puzzle.

    Returns the 'minimum value' for 'line'.
    """

    # larger than biggest result
    result = MaxResult + 1

    # first, get minimum number of symbols in 'line'
    # this sets the minimum base for the line
    unique_symbols = {}
    for ch in line:
        unique_symbols[ch] = True
    unique_symbols = unique_symbols.keys()
    min_base = len(unique_symbols)

    # generate all mappings of symbols to values
    # generate value and keep minimum
    for base in range(min_base, MaxBase+1):
        perms = itertools.permutations(AllValues[:base], min_base)
        for mapping in perms:
            index_dir = {}
            for ch in unique_symbols:
                index_dir[ch] = mapping[unique_symbols.index(ch)]

            if index_dir[line[0]] == 0:
                # but first char in line can't map to 0
                continue

            value = 0
            for ch in line:
                ch_value = index_dir[ch]
                value *= base
                value += ch_value
                if value > result:
                    break
            if value < result:
                result = value

    return result
        
def main(N, fd):
    """Solve the puzzle.

    N   is the number of datasets
    fd  is the open file to read datasets from
    """

    # create all alowable values in a list
    global AllValues
    AllValues = range(MaxBase+1)[:]

    # solve each test case
    for case in xrange(N):
        line = fd.readline().strip()
        result = solve_puzzle(line)
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

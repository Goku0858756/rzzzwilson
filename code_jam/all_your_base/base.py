#!/usr/bin/env python

"""
A program to solve the Google All Your Base puzzle.

Usage:  base.py <datafile>
"""

# determine if we are running under kernprof
# define dummy @profile if not
def fake_profile(fn):
    def wrapped(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapped

try:
    if not __builtins__.has_key('profile'):
        print("REDEFINING......")
        profile = fake_profile
except AttributeError:
    print("REDEFINING......")
    profile = fake_profile

# maximum base allowed (as only 36 legal symbols)
MaxBase = 36

# all allowable values: [1, 0, 2, 3, 4, ..., 35].
# the idea is that the minimum value for a string is to have
# the first symbol map to 1 (a requirement for a minimum value)
# and each subsequent symbol comes from [0, 2, 3, 4, ...] in order.
# this gives us a minimum value for the string.
AllValues = range(MaxBase)[:]
AllValues.remove(1)
AllValues.insert(0, 1)

@profile
def solve_puzzle(string):
    """Solve the puzzle.

    Returns the 'minimum value' for 'string'.
    """

    # first, get minimum number of symbols in 'string'
    # this length of the unique string sets the minimum base for the puzzle
    unique_symbols = ''
    for ch in string:
        if ch not in unique_symbols:
            unique_symbols += ch
    base = max(2, len(unique_symbols))	# base must be at least 2 (required)

    # create mapping: sym -> value
    # we know first sym in 'string' must be 1
    # and for the following -> 0, 2, 3, 4, ..., 35
    sym2val = dict(zip(unique_symbols, AllValues))

    # generate result
    value = 0
    for ch in string:
        value = value*base + sym2val[ch]

    return value
        
def main(N, fd):
    """Solve the puzzle.

    N   is the number of datasets
    fd  is the open file to read datasets from
    """

    # solve each test case
    for case in xrange(N):
        string = fd.readline().strip()
        result = solve_puzzle(string)
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

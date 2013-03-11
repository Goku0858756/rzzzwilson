#!/usr/bin/env python

"""
Recursive solution for the Ackermann function.
With and without optimization.

Usage: ackermann <integer> <integer>

"""

#
# For a good look at optimization of Ackermann:
# [http://en.literateprograms.org/Ackermann_function_%28Python%29]
#

import time


def ackermann_naive(m, n):
    """Return the value of Ackermann(m, n)."""

    if m == 0:
        return n + 1
    elif n == 0:
        return ackermann_naive(m-1, 1)
    else:
        return ackermann_naive(m-1, ackermann_naive(m, n-1))


ackermann_memo = {(0,0):1}

def ackermann_dict(m, n):
    """Return Ackermann(m, n) with memoisation by dict."""

    if (m, n) not in ackermann_memo:
        if m == 0:
            result = n + 1
        elif n == 0:
            result = ackermann_dict(m-1, 1)
        else:
            result = ackermann_dict(m-1, ackermann_dict(m, n-1))

        ackermann_memo[(m, n)] = result

    return ackermann_memo[(m, n)]


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 3:
        print __doc__
        sys.exit(10)

    try:
        m = int(sys.argv[1])
        n = int(sys.argv[2])
    except ValueError:
        print __doc__
        sys.exit(10)

    sys.setrecursionlimit(26000)

    start = time.time()
    result = ackermann_naive(m, n)
    delta = time.time() - start
    print('ackermann_naive(%d, %d)=%d   took %9.6fs' % (m, n, result, delta))

    start = time.time()
    result = ackermann_dict(m, n)
    delta = time.time() - start
    print(' ackermann_dict(%d, %d)=%d   took %9.6fs' % (m, n, result, delta))


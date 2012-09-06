#!/usr/bin/env python

"""
Recursive solution for the Fibonacci function.
With and without memoisation.

Usage: fibonacci <integer>
"""

import time


def fibonacci(n):
    """Return the 'n'th Fibonacci number."""

    if n == 0:
        return 0
    if n == 1:
        return 1

    return fibonacci(n-1) + fibonacci(n-2)


fib_memo = {0:0, 1:1}

def fibonacci_memo(n):
    """Return the 'n'th Fibonacci number with memoisation."""

    global fib_memo		# so we can update fib_memo

    if n not in fib_memo:
        fib_memo[n] = fibonacci_memo(n-1) + fibonacci_memo(n-2)
    return fib_memo[n]

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print __doc__
        sys.exit(10)

    try:
        number = int(sys.argv[1])
    except ValueError:
        print __doc__
        sys.exit(10)

    print '     fibonacci(%d) =' % number,
    sys.stdout.flush()
    start = time.time()
    result = fibonacci(number)
    delta = time.time() - start
    print '%d   took %9.6fs' % (result, delta)

    print 'fibonacci_memo(%d) =' % number,
    sys.stdout.flush()
    start = time.time()
    result = fibonacci_memo(number)
    delta = time.time() - start
    print '%d   took %9.6fs' % (result, delta)

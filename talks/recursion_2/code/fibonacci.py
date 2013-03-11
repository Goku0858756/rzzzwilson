#!/usr/bin/env python

"""
Recursive solution for the Fibonacci function.
With and without optimization.

Usage: fibonacci <integer>
"""

import time


def fibonacci_naive(n):
    """Return the 'n'th Fibonacci number."""

    if n == 0:
        return 0
    if n == 1:
        return 1

    return fibonacci_naive(n-1) + fibonacci_naive(n-2)


fib_memo = {0:0, 1:1}

def fibonacci_dict(n):
    """Return the 'n'th Fibonacci number with memoisation by dict."""

    global fib_memo		# so we can update fib_memo

    if n not in fib_memo:
        fib_memo[n] = fibonacci_dict(n-1) + fibonacci_dict(n-2)
    return fib_memo[n]


def fibonacci_list(n):
    """Return the 'n'th Fibonacci number with memoisation by list."""

    # initialize the list for 0 to n elements
    fib_memo = [-1] * (n + 2)	# -1 means no value yet
    fib_memo[0] = 0
    fib_memo[1] = 1

    return fib_list(n, fib_memo)

def fib_list(n, memo_list):
    """Return 'n'th Fibonacci number."""

    if memo_list[n] == -1:
        memo_list[n] = fib_list(n-1, memo_list) + fib_list(n-2, memo_list)

    return memo_list[n]

def fibonacci_tuple(n):
    """Return the 'n'th Fibonacci number using tupling."""

    (fib_n, fib_n_minus_1) = fib_tuple(n)

    return fib_n

def fib_tuple(n):
    """Return the 'n'th & 'n-1'th Fibonacci numbers."""

    if n <= 1:
        return (n, 0)		# 0 and 1 base cases

    (fib_n_minus_1, fib_n_minus_2) = fib_tuple(n-1)

    #return(           fib_n,            fib_n_minus_1)
    return (fib_n_minus_1+fib_n_minus_2, fib_n_minus_1)

def fibonacci_iter(n):
    """Return 'n'th Fibonacci number using iteration."""

    previous = 1		# 1 base case
    previous_previous = 0	# 0 base case

    for _ in xrange(n):
        (previous_previous, previous) = (previous, previous+previous_previous)

    return previous_previous


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

    start = time.time()
    result = fibonacci_naive(number)
    delta = time.time() - start
    print('fibonacci_naive(%d)=%d   took %9.6fs' % (number, result, delta))

    start = time.time()
    result = fibonacci_dict(number)
    delta = time.time() - start
    print(' fibonacci_dict(%d)=%d   took %9.6fs' % (number, result, delta))

    start = time.time()
    result = fibonacci_list(number)
    delta = time.time() - start
    print(' fibonacci_list(%d)=%d   took %9.6fs' % (number, result, delta))

    start = time.time()
    result = fibonacci_tuple(number)
    delta = time.time() - start
    print('fibonacci_tuple(%d)=%d   took %9.6fs' % (number, result, delta))

    start = time.time()
    result = fibonacci_iter(number)
    delta = time.time() - start
    print(' fibonacci_iter(%d)=%d   took %9.6fs' % (number, result, delta))








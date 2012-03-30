#!/usr/bin/env python

"""
Recursive solution to the "Tower of Hanoi" puzzle.
[http://en.wikipedia.org/wiki/Tower_of_Hanoi]

Usage: hanoi <number_of_disks>
"""


def hanoi_original(n, src, dst, tmp):
    """Move 'n' disks from 'src' to 'dst' using temporary 'tmp'."""

    if n == 1:
        print('move %s to %s' % (src, dst))	# move single disk to 'dst'
    else:
        hanoi_original(n-1, src, tmp, dst)	# move n-1 to 'tmp'
        hanoi_original(1, src, dst, tmp)	# move 1 to 'dst'
        hanoi_original(n-1, tmp, dst, src)	# finally move n-1 from 'tmp' to 'dst'

def hanoi(n, src, dst, tmp):
    """Move 'n' disks from 'src' to 'dst' using temporary 'tmp'."""

    if n > 0:
        hanoi(n-1, src, tmp, dst)		# move n-1 to 'tmp'
        print('move %s to %s' % (src, dst))	# move single disk to 'dst'
        hanoi(n-1, tmp, dst, src)		# finally move n-1 to 'dst'


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

    hanoi(number, 'A', 'B', 'C')

#!/usr/bin/env python

"""
A program to solve the Google Big City Skyline puzzle.

Usage:  test.py <datafile>
"""


def read_width_height(fd):
    """Read building width&height from a file.

    Read a character at a time to minimise memory usage.
    """

    def read_int(fd):
        """Read one integer from file."""

        string = ''
        while True:
            ch = fd.read(1)
            if ch not in '0123456789':
                break
            string += ch
        return int(string)

    width = read_int(fd)
    height = read_int(fd)

    return (width, height)

def main(N, fd):
    """Solve the puzzle.

    N   is the number of buildings
    fd  is the open file to read wisth&height from
    """

    open_blocks = {}
    current_column = 0
    current_height = 0
    max_closed_area = -1
    for _ in xrange(N):
        (width, height) = read_width_height(fd)
        if height > current_height:
            # increase in building height - start new block
            assert not open_blocks.has_key(height)
            open_blocks[height] = current_column
        elif height < current_height:
            # decrease in building height - close all closed blocks
            # maybe start new block at new height
            del_block_keys = []

            block_list = open_blocks.items()[:]
            block_list.sort()

            have_new_block = False
            for (bheight, bstartcol) in block_list:
                if bheight > height:
                    del_block_keys.append(bheight)
                    if not have_new_block:
                        if not open_blocks.has_key(height):
                            open_blocks[height] = bstartcol
                        have_new_block = True

            # close blocks
            for bheight in del_block_keys:
                bstartcol = open_blocks[bheight]
                area = bheight * (current_column - bstartcol)
                if area > max_closed_area:
                    max_closed_area = area
                del open_blocks[bheight]
        else:
            # same height as previous building - extend all blocks
            pass

        current_column += width
        current_height = height

    # check size of all open blocks, get max area
    area = max([bheight * (current_column - bstartcol) for (bheight, bstartcol) in open_blocks.items()])

    # print largest of open and closed blocks
    print('%d' % max(area, max_closed_area))


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print __doc__
        sys.exit(10)

    buildings = []
    fd = open(sys.argv[1], 'r')
    N = int(fd.readline())

    main(N, fd)

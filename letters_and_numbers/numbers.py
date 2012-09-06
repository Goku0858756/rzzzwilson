#!/usr/bin/env python

"""
Combine a set of 6 numbers ('large' and 'small') to achieve a target number.

Usage: either numbers.py <filename>
       or     numbers.py n1 n2 n3 n4 n5 n6 target

where <filename> is a file that contains one or more lines:
    n1 n2 n3 n4 n5 n6 target
"""


# a dictionary mapping mathematical operation to code
op_dict = {'+': lambda x, y: x+y,
           '-': lambda x, y: x-y,
           '*': lambda x, y: x*y,
           '/': lambda x, y: dodiv(x, y)}

def dodiv(x, y):
    """Do a divide, throwing exception if remainder is non-zero."""

    if x % y:
        raise RuntimeError

    return x/y

def evaluate(numbers, ops, target, explain=False):
    """RPN evaluate the numbers and operators.

    numbers   list of 6 numbers to evaluate
    ops       list of 5 operators
    target    desired target number
    explain   True if we are to explain the evaluation

    Return the evaluated number closest to the target.
    """

    (n1, n2, n3, n4, n5, n6) = numbers
    (o1, o2, o3, o4, o5) = ops
    delta = 99999999
    closest = 99999999

    try:
        value = op_dict[o1](n1, n2)
    except RuntimeError:
        return 99999999
    if explain:
        print('%d %s %d = %d' % (n1, o1, n2, value))
    if value == target:
        return target
    new_delta = abs(target - value)
    if new_delta < delta:
        delta = new_delta
        closest = value

    try:
        value2 = op_dict[o2](value, n3)
    except RuntimeError:
        return 99999999
    if explain:
        print('%d %s %d = %d' % (value, o2, n3, value2))
    value = value2
    if value == target:
        return target
    new_delta = abs(target - value)
    if new_delta < delta:
        delta = new_delta
        closest = value

    try:
        value2 = op_dict[o3](value, n4)
    except RuntimeError:
        return 99999999
    if explain:
        print('%d %s %d = %d' % (value, o3, n4, value2))
    value = value2
    if value == target:
        return target
    new_delta = abs(target - value)
    if new_delta < delta:
        delta = new_delta
        closest = value

    try:
        value2 = op_dict[o4](value, n5)
    except RuntimeError:
        return 99999999
    if explain:
        print('%d %s %d = %d' % (value, o4, n5, value2))
    value = value2
    if value == target:
        return target
    new_delta = abs(target - value)
    if new_delta < delta:
        delta = new_delta
        closest = value

    try:
        value2 = op_dict[o5](value, n6)
    except RuntimeError:
        return 99999999
    if explain:
        print('%d %s %d = %d' % (value, o5, n6, value2))
    value = value2
    if value == target:
        return target
    new_delta = abs(target - value)
    if new_delta < delta:
        delta = new_delta
        closest = value

    return closest

def make_ops():
    """Make all combinations of 5 operators.

    We have 6 numbers, so we need at most 5 operators.
    """

    ops = ['+', '-', '*', '/']

    for o1 in ops:
        for o2 in ops:
            for o3 in ops:
                for o4 in ops:
                    for o5 in ops:
                        yield [o1, o2, o3, o4, o5]

def make_numbers(numbers):
    """Make all combinations of numbers."""

    used = []

    for i1 in range(len(numbers)):
        used.append(i1)
        for i2 in range(len(numbers)):
            if i2 in used:
                continue
            used.append(i2)
            for i3 in range(len(numbers)):
                if i3 in used:
                    continue
                used.append(i3)
                for i4 in range(len(numbers)):
                    if i4 in used:
                        continue
                    used.append(i4)
                    for i5 in range(len(numbers)):
                        if i5 in used:
                            continue
                        used.append(i5)
                        for i6 in range(len(numbers)):
                            if i6 in used:
                                continue
                            used.append(i6)
                            yield [numbers[i1], numbers[i2], numbers[i3], numbers[i4], numbers[i5], numbers[i6],]
                            used.pop()
                        used.pop()
                    used.pop()
                used.pop()
            used.pop()
        used.pop()


if __name__ == '__main__':
    import sys

    # get puzzles in form: [[numbers, target], ...]
    if len(sys.argv) == 8:
        numbers = [sys.argv[1], sys.argv[2], sys.argv[3],
                   sys.argv[4], sys.argv[5], sys.argv[6]]
        numbers= [int(x) for x in numbers]
        target = int(sys.argv[7])
        puzzle = [[numbers, target]]
    elif len(sys.argv) == 2:
        puzzle = []
        with open(sys.argv[1], 'r') as fd:
            for line in fd:
                numbers = line.strip().split()
                numbers = [int(x) for x in numbers]
                target = numbers.pop(6)
                puzzle.append([numbers, target])
    else:
        print __doc__
        sys.exit(10)

    closest = 99999999
    closest_num = None
    closest_ops = None
    delta = 99999999

    for (numbers, target) in puzzle:
        try:
            for num in make_numbers(numbers):
                for ops in make_ops():
                    new_closest = evaluate(num, ops, target)
                    if new_closest == target:
                        print('Solution: %s %s = %d' % (str(ops), str(num), target))
                        evaluate(num, ops, target, explain=True)
                        raise RuntimeError()
                    new_delta = abs(target - new_closest)
                    if new_delta < delta:
                        delta = new_delta
                        closest = new_closest
                        closest_num = num
                        closest_ops = ops
        except RuntimeError:
            continue

        print('No solution for %s, target %d' % (str(numbers), target))

#!/usr/bin/env python

"""Run simple string concatenation speed tests."""


import time
import platform
from UserString import MutableString
from array import array
from cStringIO import StringIO


TIMES = 100000


def concat_naive_func(a, n):
    a += str(n)
    return a

def concat_naive(times):
    a = ''
    start = time.time()
    for n in xrange(times):
        a = concat_naive_func(a, n)
    delta = time.time() - start
    return delta

def concat_array_func(a, n):
    a.fromstring(str(n))

def concat_array(times):
    a = array('c')
    start = time.time()
    for n in xrange(times):
        concat_array_func(a, n)
    a = ''.join(a)
    delta = time.time() - start
    return delta

def concat_join_func(a, n):
    return a.append(str(n))

def concat_join(times):
    a = []
    start = time.time()
    for n in xrange(times):
        concat_join_func(a, n)
    a = ''.join(a)
    delta = time.time() - start
    return delta

def concat_stringio_func(a, n):
    a.write(str(n))

def concat_stringio(times):
    a = StringIO()
    start = time.time()
    for n in xrange(times):
        concat_stringio_func(a, n)
    a = a.getvalue()
    delta = time.time() - start
    return delta

if __name__ == '__main__':
    print('Using Python %s' % platform.python_version())
    print('For %d concatenations:' % TIMES)
    result = concat_naive(TIMES)
    print('        naive: %5.2fs' % result)
    time.sleep(1)
    result = concat_array(TIMES)
    print('        array: %5.2fs' % result)
    time.sleep(1)
    result = concat_join(TIMES)
    print('         join: %5.2fs' % result)
    time.sleep(1)
    result = concat_stringio(TIMES)
    print('     stringio: %5.2fs' % result)
    time.sleep(1)

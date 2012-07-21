#!/usr/bin/python

"""
The Imlac trace stuff.
"""


import time

from Globals import *
import MainCPU
import DisplayCPU


class Trace(object):
    def __init__(self, filename):
        self.tracing = True
        self.tracefile = open(filename, 'w')
        self.trace('pymlac %s trace\n\n' % PYMLAC_VERSION)
        self.trace('DPC\tDisplay\t\tPC\tMain\t\tRegs\n')
        self.trace('------  -------------   ------  --------------  '
                   '-----------------------\n')
        self.tracing = False

    def close(self):
        self.tracefile.close()

    def trace(self, msg):
        if self.tracing:
            self.tracefile.write(msg)
        
    def deimtrace(self, opcode, code):
        if self.tracing:
            self.tracefile.write('%s\t%s\t' % (opcode, code))

    def dtrace(self, opcode, address=None):
        if self.tracing:
            if address is None:
                self.tracefile.write('%s\t\t' % opcode)
            else:
                self.tracefile.write('%s\t%5.5o\t' % (opcode, address))

    def itrace(self, opcode, indirect=0, address=None):
        if self.tracing:
            char = '*' if indirect else ''
            if address is None:
                self.tracefile.write('%s\t%s\t' % (opcode, char))
            else:
                self.tracefile.write('%s\t%s%5.5o\t' % (opcode, char, address))

    def itraceend(self, dispon):
        if dispon:
            self.trace('L=%1.1o AC=%6.6o DX=%5.5o DY=%6.6o\n' %
                       (MainCPU.L, MainCPU.AC, DisplayCPU.DX, DisplayCPU.DY))
        else:
            self.trace('L=%1.1o AC=%6.6o\n' % (MainCPU.L, MainCPU.AC))

    def settrace(self, tracing):
        self.tracing = tracing

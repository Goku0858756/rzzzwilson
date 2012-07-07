#!/usr/bin/python 

"""
Class to emulate the imlac Paper Tape Reader (PTR).

We take some pains to closely emulate the *real* PTR device, even
including misuse, such as no tape mounted.  This means we must tell
the PTR object how many CPU cycles have passed (self.tick()).
"""

from Globals import *


class Ptr(object):
    """Class for imlac Paper Tape Reader (PTR)."""

    # number of chars per second we want
    CharsPerSecond = 300

    # duty cycle for PTR is 30% ready and 70% not ready
    ReadyCycles = int((CYCLES_PER_SECOND / CharsPerSecond) / 0.7) / 25
    NotReadyCycles = int((CYCLES_PER_SECOND / CharsPerSecond) / 0.3) / 25

    # no tape in reader, return 0377 (all holes see light)
    PtrEOF = 0377

    def __init__(self):
        self.motor_on = False
        self.device_ready = False
        self.filename = None
        self.at_eof = True
        self.value = self.PtrEOF
        self.cycle_count = 0

    def mount(self, filename):
        self.motor_on = False
        self.device_ready = False
        self.filename = filename
        self.open_file = open(filename, 'r')
        self.at_eof = False
        self.value = self.PtrEOF

    def dismount(self):
        self.motor_on = False
        self.device_ready = False
        if self.filename:
            self.open_file.close()
        self.filename = None
        self.at_eof = True
        self.value = self.PtrEOF

    def start(self):
        self.motor_on = True
        self.device_ready = False
        self.cycle_count = self.NotReadyCycles

    def stop(self):
        self.motor_on = False
        self.device_ready = False
        self.cycle_count = self.NotReadyCycles

    def read(self):
        return self.value

    def eof(self):
        return self.at_eof

    def tick(self, cycles):
        """Called to push PTR state along.

        cycles  number of cycles passed since last tick
        """

        # if end of tape or motor off, do nothing, state remains unchanged
        if self.at_eof or not self.motor_on:
            return

        self.cycle_count -= cycles
        if self.cycle_count <= 0:
            if self.device_ready:
                self.device_ready = False
                self.cycle_count += self.NotReadyCycles
            else:
                self.device_ready = True
                self.cycle_count += self.ReadyCycles
                self.value = self.open_file.read(1)
                if len(self.value) < 1:
                    # EOF on input file, pretend end of tape
                    self.at_eof = True
                    self.value = self.PtrEOF
                else:
                    self.value = ord(self.value)

    def ready(self):
        return self.device_ready


if __name__ == '__main__':
    """ Test the emulation of the PTR device """

    import sys
    import log
    log = log.Log('ptr.log', log.Log.DEBUG)

    ptr = Ptr()
    ptr.mount('test1.ptp')
    ptr.start()
    while not ptr.eof():
        timeout = 1000000
        while not ptr.ready():
            ptr.tick(2)
            timeout -= 1
            if timeout < 0:
                print('TIMEOUT')
                sys.exit(0)
        char = ptr.read()
        log('byte is \\%3.3o (0x%02x)' % (char, char))
        timeout = 1000000
        while ptr.ready():
            ptr.tick(2)
            timeout -= 1
            if timeout < 0:
                print('TIMEOUT')
                sys.exit(0)


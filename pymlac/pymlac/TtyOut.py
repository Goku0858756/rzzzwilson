#!/usr/bin/python 

"""
Class to emulate the Output TTY (TTYOUT).
"""


from Globals import *


class TtyOut(object):
    # define various internal states
    DEVICE_NOT_READY = 0
    DEVICE_READY = 1
    TTYOUT_CHARS_PER_SECOND = 1000
    DEVICE_NOT_READY_CYCLES = int(CYCLES_PER_SECOND / TTYOUT_CHARS_PER_SECOND)

    def __init__(self):
        self.filename = None
        self.open_file = None
        self.open_file = 0
        self.cycle_count = 0
        self.state = self.DEVICE_NOT_READY

    def mount(self, filename):
        self.filename = filename
        self.open_file = open(filename, 'w')
        self.state = self.DEVICE_READY

    def dismount(self):
        if self.open_file:
            self.open_file.close()
        self.filename = None
        self.open_file = None
        self.state = self.DEVICE_NOT_READY

    def write(self, char):
        self.open_file.write(char)
        self.cycle_count = self.DEVICE_NOT_READY_CYCLES

    def ready(self):
        return (self.state != self.DEVICE_NOT_READY)

    def clear(self):
        self.state = self.DEVICE_NOT_READY

    def tick(self, cycles):
        if (self.state == self.DEVICE_NOT_READY):
            self.cycle_count -= cycles
            if self.cycle_count <= 0:
                self.state = self.DEVICE_READY

def test_main():
    """ Test the emulation of the TTYOUT device """
    ttyout = TtyOut()
    ttyout.mount('testttyout')
    while not ttyout.ready():
        ttyout.tick(2)
    char = ttyout.write('A')
    ttyout.clear()
    while not ttyout.ready():
        ttyout.tick(2)
    char = ttyout.write('B')
    ttyout.clear()
    while not ttyout.ready():
        ttyout.tick(2)
    char = ttyout.write('C')
    ttyout.clear()
    while not ttyout.ready():
        ttyout.tick(2)
    char = ttyout.write('\n')
    ttyout.clear()
    while not ttyout.ready():
        ttyout.tick(2)
    char = ttyout.write('X')
    ttyout.clear()
    while not ttyout.ready():
        ttyout.tick(2)
    char = ttyout.write('Y')
    ttyout.clear()
    while not ttyout.ready():
        ttyout.tick(2)
    char = ttyout.write('Z')
    ttyout.clear()
    while not ttyout.ready():
        ttyout.tick(2)
    char = ttyout.write('.')
    while not ttyout.ready():
        ttyout.tick(2)
    ttyout.dismount()

if __name__ == '__main__':
    test_main()

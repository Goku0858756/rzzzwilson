#!/usr/bin/python 

"""
Class to emulate the Input TTY (TTYIN).
"""


from Globals import *


class TtyIn(object):
    # define various internal states
    DEVICE_NOT_READY = 0
    DEVICE_READY = 1
    TTYIN_CHARS_PER_SECOND = 1000
    DEVICE_READY_CYCLES = int(CYCLES_PER_SECOND / TTYIN_CHARS_PER_SECOND)

    def __init__(self):
        self.filename = None
        self.open_file = None
        self.value = 0
        self.atEOF = 1
        self.cycle_count = 0
        self.isready = self.DEVICE_NOT_READY

    def mount(self, filename):
        self.filename = filename
        self.open_file = open(filename, 'r')
        self.value = 0
        self.atEOF = 0
        self.cycle_count = self.DEVICE_READY_CYCLES
        self.isready = self.DEVICE_NOT_READY

    def dismount(self):
        if self.open_file:
            self.open_file.close()
        self.filename = None
        self.open_file = None
        self.value = 0
        self.atEOF = 1
        self.isready = self.DEVICE_NOT_READY

    def read(self):
        return self.value

    def ready(self):
        return (self.isready == self.DEVICE_READY)

    def clear(self):
        self.isready = self.DEVICE_NOT_READY

    def tick(self, cycles):
        if (not self.atEOF):
            self.cycle_count -= cycles
            if self.cycle_count <= 0:
                self.cycle_count = self.DEVICE_READY_CYCLES
                self.value = self.open_file.read(1)
                self.isready = self.DEVICE_READY
                if len(self.value) < 1:
                    self.atEOF = 1
                    self.value = 0
                    self.cycle_count = 0
                    self.isready = self.DEVICE_NOT_READY

def test_main():
    """ Test the emulation of the TTYIN device """
    ttyin = TtyIn()
    ttyin.mount('test')
    while 1:
        while not ttyin.ready():
            ttyin.tick(2)
        char = ttyin.read()
        print 'is "' + char + '"'
        ttyin.clear()

if __name__ == '__main__':
    test_main()

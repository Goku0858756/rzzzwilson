#!/usr/bin/python 

"""
Class to emulate the Paper Tape Punch (PTP).
"""


from Globals import *


class Ptp(object):
    # define various internal states
    MOTOR_ON = 1
    MOTOR_OFF = 0
    DEVICE_NOT_READY = 0
    DEVICE_READY = 1
    PTP_CHARS_PER_SECOND = 30
    DEVICE_NOT_READY_CYCLES = int(CYCLES_PER_SECOND / PTP_CHARS_PER_SECOND)

    def __init__(self):
        self.motor_state = self.MOTOR_OFF
        self.device_state = self.DEVICE_NOT_READY
        self.filename = None
        self.open_file = None

    def mount(self, filename):
        self.motor_state = self.MOTOR_OFF
        self.device_state = self.DEVICE_NOT_READY
        self.filename = filename
        self.open_file = open(filename, 'w')

    def dismount(self):
        self.motor_state = self.MOTOR_OFF
        self.device_state = self.DEVICE_NOT_READY
        if self.open_file:
            self.open_file.close()
        self.filename = None
        self.open_file = None

    def start(self):
        self.motor_state = self.MOTOR_ON
        self.device_state = self.DEVICE_NOT_READY
        self.cycle_count = self.DEVICE_NOT_READY_CYCLES

    def stop(self):
        self.motor_state = self.MOTOR_OFF
        self.device_state = self.DEVICE_NOT_READY

    def write(self, ch):
        self.device_state = self.DEVICE_NOT_READY
        self.cycle_count = self.DEVICE_NOT_READY_CYCLES
        self.open_file.write(ch)

    def tick(self, cycles):
        if self.motor_state == self.MOTOR_OFF or not self.open_file:
            self.device_state = self.DEVICE_NOT_READY
            return

        self.cycle_count -= cycles
        if self.cycle_count <= 0:
            self.device_state = self.DEVICE_READY

    def ready(self):
        return self.device_state == self.DEVICE_READY

def test_main():
    """ Test the emulation of the PTP device """
    ptp = Ptp()
    ptp.mount('testptp')
    ptp.start()
    while not ptp.ready():
        ptp.tick(2)
    char = ptp.write('A')
    while not ptp.ready():
        ptp.tick(2)
    char = ptp.write('B')
    while not ptp.ready():
        ptp.tick(2)
    char = ptp.write('C')
    while not ptp.ready():
        ptp.tick(2)
    char = ptp.write('\n')
    while not ptp.ready():
        ptp.tick(2)
    char = ptp.write('X')
    while not ptp.ready():
        ptp.tick(2)
    char = ptp.write('Y')
    while not ptp.ready():
        ptp.tick(2)
    char = ptp.write('Z')
    while not ptp.ready():
        ptp.tick(2)
    char = ptp.write('.')
    while not ptp.ready():
        ptp.tick(2)
    ptp.dismount()

if __name__ == '__main__':
    test_main()

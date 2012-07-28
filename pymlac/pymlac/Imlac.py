#!/usr/bin/python

"""
The Imlac emulation object.
"""


import sys

from Globals import *

import Ptr, Ptp,TtyIn, TtyOut
import Kbd
import Memory
import MainCPU
import DisplayCPU
import Display
import Panel
import Trace


class Imlac(object):
    def __init__(self, run_address, tracefile, tracestart, traceend,
                 boot_rom=None, corefile=None):
        self.main_running = 1
        self.display_running = 0
        self.memory = Memory.Memory(boot_rom, corefile)
        self.trace = Trace.Trace(tracefile)
        self.tracestart = tracestart
        self.traceend = traceend
        self.kbd = Kbd.Kbd()
        self.ptr = Ptr.Ptr()
        self.ptp = Ptp.Ptp()
        self.ttyin = TtyIn.TtyIn()
        self.ttyout = TtyOut.TtyOut()
#        self.font_data = pygame.font.Font(None, 21)
#        self.font_label = pygame.font.Font(None, 24)
#        self.panel = Panel.Panel(PYMLAC_VERSION, self.font_data, self.font_label)
#        self.display = Display.Display(screen)
        self.displaycpu = DisplayCPU.DisplayCPU(self.trace, self.memory,
#                                                self.panel, self.display,
                                                self.kbd, self.ptr, self.ptp,
                                                self.ttyin, self.ttyout)
        self.main = MainCPU.MainCPU(self.trace, self.memory,
#                                    self.panel, self.displaycpu, self.display,
                                    self.displaycpu,
                                    self.kbd, self.ptr, self.ptp, self.ttyin,
                                    self.ttyout, run_address)
    def close(self, corefile=None):
        if corefile:
            self.memory.savecore(corefile)
        sys.exit()

    def set_ROM(self, type):
        self.memory.set_ROM(type)

    def ptr_mount(self, filename):
        self.ptr.mount(filename)

    def ptp_mount(self, filename):
        self.ptp.mount(filename)

    def ttyin_mount(self, filename):
        self.ttyin.mount(filename)

    def ttyout_mount(self, filename):
        self.ttyout.mount(filename)

    def ptr_dismount(self):
        self.ptr.dismount()

    def ptp_dismount(self):
        self.ptp.dismount()

#    def pump(self):
#        pass
#        self.panel.updateAC(MainCPU.AC)
#        self.panel.updatePC(MainCPU.PC)

    def ttyin_dismount(self):
        self.ttyin.dismount()

    def ttyout_dismount(self):
        self.ttyout.dismount()

    def ptr_start(self):
        self.ptr.start()

    def ptp_start(self):
        self.ptp.start()

    def ttyin_start(self):
        self.ttyin.start()

    def ttyout_start(self):
        self.ttyout.start()

    def ptr_stop(self):
        self.ptr.stop()

    def ptp_stop(self):
        self.ptp.stop()

    def ttyin_stop(self):
        self.ttyin.stop()

    def ttyout_stop(self):
        self.ttyout.stop()

    def set_boot(self, romtype):
        pass

    def run(self, pc=None):
        self.running = 1
        if not pc is None:
            #regs.pc = MEMORY_MASK(pc)
            regs.pc = pc

    def __tick_all(self, cycles):
        self.ptr.tick(cycles)
        self.ptp.tick(cycles)
        self.ttyin.tick(cycles)
        self.ttyout.tick(cycles)
#        self.display.tick(cycles)

    def execute_once(self):
        if self.traceend == None:
            if MainCPU.PC == self.tracestart:
                self.trace.settrace(True)
        else:
            self.trace.settrace(MainCPU.PC >= self.tracestart and MainCPU.PC <= self.traceend)

        if self.displaycpu.ison():
            self.trace.trace('%6.6o' % DisplayCPU.DPC)
        self.trace.trace('\t')

        instruction_cycles = self.displaycpu.execute_one_instruction()

        self.trace.trace('%6.6o\t' % MainCPU.PC)

        instruction_cycles += self.main.execute_one_instruction()

        self.trace.itraceend(self.displaycpu.ison())

        self.__tick_all(instruction_cycles)

        if not self.displaycpu.ison() and not self.main.running:
            return 0

        return instruction_cycles

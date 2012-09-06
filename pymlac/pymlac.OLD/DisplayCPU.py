#!/usr/bin/python

"""
The Imlac display CPU.
"""


import sys

import pygame
from pygame.locals import *

from Globals import *

import Trace


######
# The Display CPU registers
######

DPC = 0				# display CPU program counter
DS = 0100000			# display CPU ???
DRS = [0, 0, 0, 0, 0, 0, 0, 0]	# display CPU ???
DRSindex = 0			# display CPU ???
DIB = 0				# display CPU ???
DX = 0				# display CPU draw X register
DY = 0				# display CPU draw Y register


######
# The Display CPU object
######

class DisplayCPU(object):
    MODE_NORMAL = 0
    MODE_DEIM = 1

    def __init__(self, trace, memory, panel, display,
                 kbd, ptr, ptp, ttyin, ttyout):
        self.trace = trace
        self.memory = memory
        self.panel = panel
        self.display = display
        self.kbd = kbd
        self.ptr = ptr
        self.ptp = ptp
        self.ttyin = ttyin
        self.ttyout = ttyout
        self.mode = self.MODE_NORMAL
        self.running = 0

    def DEIMdecode(self, byte):
        """Decode a DEIM byte"""

        result = ''
        if byte & 0x80:
            if byte & 0x40: result += 'B'
            else:           result += 'D'
            if byte & 0x20: result += '-'
            result += '%d' % ((byte >> 3) & 0x03)
            if byte & 0x04: result += '-'
            result += '%d' % (byte & 0x03)
        else:
            if byte == 0111:   result += 'N'
            elif byte == 0151: result += 'R'
            elif byte == 0171: result += 'F'
            elif byte == 0200: result += 'P'
            else:              result += 'A%3.3o' % byte
        return result

    def doDEIMByte(self, byte):
        global DPC, DX, DY, DRSindex

        if byte & 0x80:			# increment?
            prevDX = DX
            prevDY = DY
            if byte & 0x20:
                DX -= (byte & 0x18) >> 3
            else:
                DX += (byte & 0x18) >> 3
            if byte & 0x04:
                DY -= (byte & 0x03)
            else:
                DY += (byte & 0x03)
            if byte & 0x40:
                self.display.draw(0, prevDX, prevDY, DX, DY)
        else:				# micro instructions
            if byte & 0x40:
                self.mode = self.MODE_NORMAL
            if byte & 0x20:		# DRJM
                if DRSindex <= 0:
                    print '\nDRS stack underflow at display address %6.6o' % (DPC - 1)
                    illegal()
                DRSindex -= 1
                DPC = DRS[DRSindex]
            if byte & 0x10:
                DX += 0x08
            if byte & 0x08:
                DX &= 0xfff8
            if byte & 0x02:
                DY += 0x10
            if byte & 0x01:
                DY &= 0xfff0

    def execute_one_instruction(self):
        global DPC

        if self.running == 0:
            self.trace.dtrace('')
            return 0

        instruction = self.memory.get(DPC, 0)
        DPC = MASK_MEM(DPC + 1)

        if self.mode == self.MODE_DEIM:
            self.trace.trace(self.DEIMdecode(instruction >> 8) + '\t')
            self.doDEIMByte(instruction >> 8)
            if self.mode == self.MODE_DEIM:
                self.trace.trace(self.DEIMdecode(instruction & 0xff) + '\t')
                self.doDEIMByte(instruction & 0xff)
            else:
                self.trace.trace('\t')
            return 1

        opcode = instruction >> 12
        address = instruction & 007777

        if   opcode == 000:	return self.page00(instruction)
        elif opcode == 001:     return self.i_DLXA(address)
        elif opcode == 002:     return self.i_DLYA(address)
        elif opcode == 003:     return self.i_DEIM(address)
        elif opcode == 004:     return self.i_DLVH(address)
        elif opcode == 005:     return self.i_DJMS(address)
        elif opcode == 006:     return self.i_DJMP(address)
        elif opcode == 007:     return self.illegal(instruction)
        else:                   self.illegal(instruction)

    def illegal(self, instruction=None):
        if instruction:
            print 'Illegal display instruction (', '%6.6o' % instruction, ') at address', '%6.6o' % (DPC - 1)
        else:
            print 'Illegal display instruction at address', '%6.6o' % (DPC - 1)
        sys.exit(0)

    def ison(self):
        return self.running

    def i_DDXM(self):
        global DX

        DX -= 040
        self.trace.dtrace('DDXM')

    def i_DDYM(self):
        global DY

        DY -= 040
        self.trace.dtrace('DDYM')

    def i_DEIM(self, address):
        self.mode = self.MODE_DEIM
        self.trace.deimtrace('DEIM', self.DEIMdecode(address & 0377))
        self.doDEIMByte(address & 0377)
        return 1

    def i_DHLT(self):
        self.running = 0
        self.display.flip()
        self.trace.dtrace('DHLT')

    def i_DHVC(self):
        self.trace.dtrace('DHVC')

    def i_DIXM(self):
        global DX

        DX += 04000
        self.trace.dtrace('DIXM')

    def i_DIYM(self):
        global DY

        DY += 04000
        self.trace.dtrace('DIYM')

    def i_DJMP(self, address):
        global DPC, DIB

        DPC = MASK_MEM(address + (DIB << 12))
        self.trace.dtrace('DJMP', address)
        return 1

    def i_DJMS(self, address):
        global DPC, DRSindex, DIB

        if DRSindex >= 8:
            print 'DRS stack overflow at display address %6.6o' % (DPC - 1)
            self.illegal()
        DRS[DRSindex] = DPC
        DRSindex += 1
        DPC = MASK_MEM(address + (DIB << 12))
        self.trace.dtrace('DJMS', address)
        return 1

    def i_DLXA(self, address):
        global DX

        DX = address
        self.trace.dtrace('DLXA', address)
        return 1

    def i_DLYA(self, address):
        global DY

        DY = address
        self.trace.dtrace('DLYA', address)
        return 1

    def i_DLVH(self, word1):
        global DPC, DX, DY

        word2 = self.memory.get(DPC, 0)
        DPC = MASK_MEM(DPC + 1)
        word3 = self.memory.get(DPC, 0)
        DPC = MASK_MEM(DPC + 1)

        dotted = word2 & 040000
        beamon = word2 & 020000
        negx = word3 & 040000
        negy = word3 & 020000
        ygtx = word3 & 010000

        M = word2 & 007777
        N = word3 & 007777

        prevDX = DX
        prevDY = DY

        if ygtx:		# M is y, N is x
            if negx:
                DX -= N
            else:
                DX += N
            if negy:
                DY -= M
            else:
                DY += M
        else:			# M is x, N is y
            if negx:
                DX -= M
            else:
                DX += M
            if negy:
                DY -= N
            else:
                DY += N

        self.display.drawline(dotted, prevDX, prevDY, DX, DY)
        self.trace.dtrace('DLVH')
        return 3

    def i_DRJM(self):
        global DPC, DRSindex

        if DRSindex <= 0:
           print '\nDRS stack underflow at display address %6.6o' % (DPC - 1)
           illegal()
        DRSindex -= 1
        DPC = DRS[DRSindex]
        self.trace.dtrace('DRJM')

    def i_DSTB(self, block):
        global DIB

        DIB = block
        self.trace.dtrace('DSTB\t%d' % block)

    def i_DSTS(self, scale):
        global Scale

        if scale == 0:
            Scale = 0.5
        elif scale == 1:
            Scale = 1.0
        elif scale == 2:
            Scale = 2.0
        elif scale == 3:
            Scale = 3.0
        else:
            illegal()
        self.trace.dtrace('DSTS', scale)

    def page00(self, instruction):
        if instruction == 000000:		# DHLT
            self.i_DHLT()
        elif instruction == 004000:		# DNOP
            self.trace.dtrace('DNOP')
        elif instruction == 004004:		# DSTS 0
            self.i_DSTS(0)
        elif instruction == 004005:		# DSTS 1
            self.i_DSTS(1)
        elif instruction == 004006:		# DSTS 2
            self.i_DSTS(2)
        elif instruction == 004007:		# DSTS 3
            self.i_DSTS(3)
        elif instruction == 004010:		# DSTB 0
            self.i_DSTB(0)
        elif instruction == 004011:		# DSTB 1
            self.i_DSTB(1)
        elif instruction == 004040:		# DRJM
            self.i_DRJM()
        elif instruction == 004100:		# DDYM
            self.i_DDYM()
        elif instruction == 004200:		# DDXM
            self.i_DDXM()
        elif instruction == 004400:		# DIYM
            self.i_DIYM()
        elif instruction == 005000:		# DIXM
            self.i_DIXM()
        elif instruction == 006000:		# DHVC
            self.i_DHVC()
        else:
            self.illegal(instruction)
        return 1

    def start(self):
        self.running = 1

    def stop(self):
        self.running = 0

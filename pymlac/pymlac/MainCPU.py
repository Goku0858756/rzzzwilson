#!/usr/bin/python

"""
The Imlac main CPU.
"""


import sys

import pygame
from pygame.locals import *

from Globals import *
import DisplayCPU

import Trace


######
# The main CPU registers
######

PC = 040			# main CPU program counter
L = 0				# main CPU link register
AC = 0				# main CPU accumulator
Sync40Hz = 1			# main CPU 40Hz flag register

# address of base of local code block
BlockBase = 0


class MainCPU(object):
    """The imlac CPUU object."""

    def __init__(self, trace, memory, displaycpu,
                 kbd, ptr, ptp, ttyin, ttyout, run):
        self.trace = trace
        self.memory = memory
        self.displaycpu = displaycpu
        self.kbd = kbd
        self.ptr = ptr
        self.ptp = ptp
        self.ttyin = ttyin
        self.ttyout = ttyout
        self.running = True
        self.run_address = run
        self.dispatch = {0000: self.page000,
                         0004: self.i_LAW,
                         0010: self.i_JMP,
                         0014: self.illegal,
                         0020: self.i_DAC,
                         0024: self.i_XAM,
                         0030: self.i_ISZ,
                         0034: self.i_JMS,
                         0040: self.illegal,
                         0044: self.i_AND,
                         0050: self.i_IOR,
                         0054: self.i_XOR,
                         0060: self.i_LAC,
                         0064: self.i_ADD,
                         0070: self.i_SUB,
                         0074: self.i_SAM,
                         0100: self.page100,
                         0104: self.i_LWC,
                         0110: self.i_JMP,
                         0114: self.illegal,
                         0120: self.i_DAC,
                         0124: self.i_XAM,
                         0130: self.i_ISZ,
                         0134: self.i_JMS,
                         0140: self.illegal,
                         0144: self.i_AND,
                         0150: self.i_IOR,
                         0154: self.i_XOR,
                         0160: self.i_LAC,
                         0164: self.i_ADD,
                         0170: self.i_SUB,
                         0174: self.i_SAM, }

        self.page001instructions = {0001003: self.i_DLA,
                                    0001012: self.i_DOF,
                                    0001021: self.i_KRB,
                                    0001022: self.i_KCF,
                                    0001023: self.i_KRC,
                                    0001031: self.i_RRB,
                                    0001032: self.i_RCF,
                                    0001033: self.i_RRC,
                                    0001041: self.i_TPR,
                                    0001042: self.i_TCF,
                                    0001043: self.i_TPC,
                                    0001051: self.i_HRB,
                                    0001052: self.i_HOF,
                                    0001061: self.i_HON,
                                    0001071: self.i_SCF,
                                    0001072: self.i_IOS,
                                    0001271: self.i_PUN,
                                    0001274: self.i_PSF, }

        self.page002instructions = {0002001: self.i_ASZ,
                                    0002002: self.i_ASP,
                                    0002004: self.i_LSZ,
                                    0002010: self.i_DSF,
                                    0002020: self.i_KSF,
                                    0002040: self.i_RSF,
                                    0002100: self.i_TSF,
                                    0002200: self.i_SSF,
                                    0002400: self.i_HSF, }

        self.page003instructions = {000: self.i_RAL,
                                    004: self.i_RAR,
                                    010: self.i_SAL,
                                    014: self.i_SAR,
                                    020: self.i_DON, }

    def EFFADDR(self, address):
        return BlockBase | address

    def execute_one_instruction(self):
        """Execute one MAIN instruction, return # cycles used"""

        global PC, BlockBase

        if not self.running:
            print('MainCPU halted')
            return 0

        # get instruction word to execute, advance PC
        instruction = self.memory.get(PC, False)
        BlockBase = PC & ADDRHIGHMASK
        PC = MASK_MEM(PC + 1)

        # break instruction into opcode and address
        indirect = instruction >> 15
        opcode = (instruction >> 11) << 2	# note, includes indirect bit
        address = instruction & 03777

        return self.dispatch[opcode](indirect, address, instruction)

    def illegal(self, indirect, address, instruction=None):
        if instruction:
            msg = 'Illegal instruction (%6.6o) at address %6.6o' % (instruction, PC-1) 
        else:
            msg = 'Illegal instruction at address %6.6o' % (PC-1)
        raise RuntimeError(msg)

    def i_HLT(self, indirect, address, instruction):
        self.trace.itrace('HLT', indirect, address)
        return 1

    def i_ADD(self, indirect, address, instruction):
        global AC, L

        effaddress = self.EFFADDR(address)
        AC += self.memory.get(address, indirect)
        if AC & OVERFLOWMASK:
            L = not L
            AC &= WORDMASK
        self.trace.itrace('ADD', indirect, address)
        return 3 if indirect else 2

    def i_AND(self, indirect, address, instruction):
        global AC

        AC &= self.memory.get(address, indirect)
        self.trace.itrace('AND', indirect, address)
        return 3 if indirect else 2

    def i_ASP(self):
        global PC

        if AC & HIGHBITMASK:
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('ASP')
        return 1

    def i_ASZ(self):
        global PC

        if AC == 0:
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('ASZ')
        return 1

    def i_DAC(self, indirect, address, instruction):
        address = self.EFFADDR(address)
        self.memory.put(AC, address, indirect)
        self.trace.itrace('DAC', indirect, address)
        return 3 if indirect else 2

    def i_DLA(self):
        DisplayCPU.DPC = AC
        self.trace.itrace('DLA')
        return 1

    def i_DOF(self):
        self.displaycpu.stop()
        self.trace.itrace('DOF')
        return 1

    def i_DON(self, ignore=None):
        DisplayCPU.DRSindex = 0
        self.displaycpu.start()
        self.trace.itrace('DON')
        return 1

    def i_DSF(self):
        global PC

        if self.displaycpu.ison():
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('DSF')
        return 1

    def i_DSN(self):
        global PC

        if not self.displaycpu.ison():
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('DSN')
        return 1

    def i_HOF(self):
        self.ptr.stop()
        self.trace.itrace('HOF')
        return 1

    def i_HON(self):
        self.ptr.start()
        self.trace.itrace('HON')
        return 1

    def i_HRB(self):
        global AC

        AC |= self.ptr.read()
        self.trace.itrace('HRB')
        return 1

    def i_HSF(self):
        global PC

        if self.ptr.ready():
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('HSF')
        return 1

    def i_HSN(self):
        global PC

        if not self.ptr.ready():
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('HSN')
        return 1

    def i_IOR(self, indirect, address, instruction):
        global AC

        AC |= self.memory.get(address, indirect)
        self.trace.itrace('IOR', indirect, address)
        return 3 if indirect else 2

    def i_IOS(self):
        self.trace.itrace('IOS')
        return 1

    def i_ISZ(self, indirect, address, instruction):
        global PC

        value = (self.memory.get(address, indirect) + 1) & WORDMASK
        self.memory.put(value, address, False)
        if value == 0:
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('ISZ', indirect, address)
        return 3 if indirect else 2

    def i_JMP(self, indirect, address, instruction):
        global PC

        jmpaddr = self.EFFADDR(address)
        if indirect:
            jmpaddr = self.memory.get(jmpaddr, False)
        PC = jmpaddr & PCMASK
        self.trace.itrace('JMP', indirect, address)
        return 3 if indirect else 2

    def i_JMS(self, indirect, address, instruction):
        global PC

        jmsaddr = self.EFFADDR(address)
        if indirect:
            jmsaddr = self.memory.get(jmsaddr, False)
        self.memory.put(PC, jmsaddr, False)
        PC = (jmsaddr + 1) & PCMASK
        self.trace.itrace('JMS', indirect, address)
        return 3 if indirect else 2

    def i_KCF(self):
        self.kbd.clear()
        self.trace.itrace('KCF')
        return 1

    def i_KRB(self):
        global AC

        AC |= self.kbd.read()
        self.trace.itrace('KRB')
        return 1

    def i_KRC(self):
        global AC

        AC |= self.kbd.read()
        self.kbd.clear()
        self.trace.itrace('KRC')
        return 1

    def i_KSF(self):
        global PC

        if self.kbd.ready():
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('KSF')
        return 1

    def i_KSN(self):
        global PC

        if not self.kbd.ready():
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('KSN')
        return 1

    def i_LAC(self, indirect, address, instruction):
        global AC

        AC = self.memory.get(address, indirect)
        self.trace.itrace('LAC', indirect, address)
        return 3 if indirect else 2

    def i_LAW(self, indirect, address, instruction):
        global AC

        AC = address
        self.trace.itrace('LAW', 0, address)
        return 1

    def i_LDA(self):
        global AC

        AC = self.dataswitches.read()
        self.trace.itrace('LDA')
        return 1

    def i_LSZ(self):
        global PC

        if L == 0:
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('LSZ')
        return 1

    def i_LWC(self, indirect, address, instruction):
        global AC

        AC = ((~address) + 1) & WORDMASK
        self.trace.itrace('LWC', 0, address)
        return 1

    def i_ODA(self):
        global AC

        AC |= self.dataswitches.read()
        self.trace.itrace('ODA')
        return 1

    def i_PSF(self):
        global PC

        if self.ptp.ready():
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('PSF')
        return 1

    def i_PUN(self):
        self.ptp.write(PC & 0xff)
        self.trace.itrace('PUN')
        return 1

    def i_RAL(self, shift):
        global AC, L

        if shift == 1:
            newl = AC >> 15
            newac = AC << 1 + L
        elif shift == 2:
            highbits = AC >> 15
            newl = (AC >> 14) & 1
            newac = (((AC << 1) + L) << 1) + highbits
        elif shift == 3:
            highbits = AC >> 14
            newl = (AC >> 13) & 1
            newac = (((AC << 1) + L) << 2) + highbits

        L = newl
        AC = newac & WORDMASK
        self.trace.itrace('RAL', 0, shift)
        return 1

    def i_RAR(self, shift):
        global AC, L

        if shift == 1:
            newl = AC & 1
            newac = AC >> 1 + L << 15
        elif shift == 2:
            lowbits = AC & 1
            newl = (AC >> 1) & 1
            newac = (((AC >> 1) + L << 15) >> 1) + lowbits << 15
        elif shift == 3:
            lowbits = AC & 3
            newl = (AC >> 2) & 1
            newac = (((AC >> 1) + L << 15) >> 2) + lowbits << 14

        shift.regs.L = newl
        shift.regs.AC = newac & WORDMASK
        self.trace.itrace('RAR', 0, shift)
        return 1

    def i_RCF(self):
        self.ttyin.clear()
        self.trace.itrace('RCF')
        return 1

    def i_RRB(self):
        global AC

        AC |= self.ttyin.read()
        self.trace.itrace('RRB')
        return 1

    def i_RRC(self):
        global AC

        AC |= self.ttyin.read()
        self.ttyin.clear()
        self.trace.itrace('RRC')
        return 1

    def i_RSF(self):
        global PC

        if self.ttyin.ready():
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('RSF')
        return 1

    def i_RSN(self):
        global PC

        if not self.ttyin.ready():
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('RSN')
        return 1

    def i_SAL(self, shift):
        global AC

        AC = (AC << shift) & WORDMASK
        self.trace.itrace('SAL', 0, shift)
        return 1

    def i_SAM(self, indirect, address, instruction):
        global PC

        samaddr = self.EFFADDR(address)
        if indirect:
            samaddr = self.memory.get(samaddr, False)
        if AC == self.memory.get(samaddr, False):
            PC = (PC + 1) & PCMASK
        self.trace.itrace('SAM', indirect, address)
        return 3 if indirect else 2

    def i_SAR(self, shift):
        global AC

        AC >>= shift
        self.trace.itrace('SAR', 0, shift)
        return 1

    def i_SCF(self):
        global Sync40Hz

        Sync40Hz = 0
        self.trace.itrace('SCF')
        return 1

    def i_SSF(self):
        global PC

        if self.display.ready():	# skip if 40Hz sync on
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('SSF')
        return 1

    def i_SSN(self):
        global PC

        if not self.display.ready():
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('SSN')
        return 1

    def i_SUB(self, indirect, address, instruction):
        global AC

        effaddr = self.EFFADDR(address)
        if indirect:
            effaddr = self.memory.get(effaddr, False)
        AC = (AC - self.memory.get(effaddr, False)) & WORDMASK
        self.trace.itrace('SUB', indirect, address)
        return 3 if indirect else 2

    def i_TCF(self):
        self.ttyout.clear()
        self.trace.itrace('TCF')
        return 1

    def i_TPC(self):
        self.ttyout.write(AC & 0xff)
        self.ttyout.clear()
        self.trace.itrace('TPC')
        return 1

    def i_TPR(self):
        self.ttyout.write(AC & 0xff)
        self.trace.itrace('TPR')
        return 1

    def i_TSF(self):
        global PC

        if self.ttyout.ready():
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('TSF')
        return 1

    def i_TSN(self):
        global PC

        if not self.ttyout.ready():
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('TSN')
        return 1

    def i_XAM(self, indirect, address, instruction):
        global AC

        if indirect:
            address = self.memory.get(address, False)
        tmp = self.memory.get(address, False)
        self.memory.put(AC, address, False)
        AC = tmp
        self.trace.itrace('XAM', indirect, address)
        return 3 if indirect else 2

    def i_XOR(self, indirect, address, instruction):
        global AC

        AC ^= self.memory.get(address, indirect)
        self.trace.itrace('XOR', indirect, address)
        return 3 if indirect else 2

    # this is fiddly because we want to trace the
    # encoded multiple instructions sensibly.
    def micro(self, instruction):
        global PC, AC, L

        if instruction == 0100000:		
            self.trace.itrace('NOP')
        elif instruction == 0100001:
            AC = 0
            self.trace.itrace('CLA')
        elif instruction == 0100002:
            AC = (~AC) & WORDMASK
            self.trace.itrace('CMA')
        elif instruction == 0100003:
            AC = 0
            AC = (~AC) & WORDMASK
            self.trace.itrace('STA')
        elif instruction == 0100004:
            newac = AC + 1
            if newac & OVERFLOWMASK:
                L = not L
            AC = newac & WORDMASK
            self.trace.itrace('IAC')
        elif instruction == 0100005:
            AC = 1
            self.trace.itrace('COA')
        elif instruction == 0100006:
            AC = (~AC) & WORDMASK
            newac = AC + 1
            if newac & OVERFLOWMASK:
                L = not L
            AC = newac & WORDMASK
            self.trace.itrace('CIA')
        elif instruction == 0100010:
            L = 0
            self.trace.itrace('CLL')
        elif instruction == 0100011:
            AC = 0
            L = 0
            self.trace.itrace('CAL')
        elif instruction == 0100020:
            L = (~L) & 1
            self.trace.itrace('CMA')
        elif instruction == 0100030:
            L = 1
            self.trace.itrace('STL')
        elif instruction == 0100040:
            AC |= self.dataswitches.read()
            self.trace.itrace('ODA')
        elif instruction == 0100041:
            AC = 0
            AC |= DisplayCPU.DS
            self.trace.itrace('LDA')
        else:		# bit-mapped operations
            combined = []
            if instruction & 0100001:
                AC = 0
                combined.append('CLA')
            if instruction & 0100010:
                L = 0
                combined.append('CLL')
            if instruction & 0100002:
                AC = (~AC) & WORDMASK
                combined.append('CMA')
            if instruction & 0100020:
                L = (~L) & 1
                combined.append('CML')
            if instruction & 0100004:
                newac = AC + 1
                if newac & OVERFLOWMASK:
                    L = not L
                AC = newac & WORDMASK
                combined.append('IAC')
            if instruction & 0100040:
                AC |= self.dataswitches.read()
                combined.append('ODA')
            if (instruction & 0100000) == 0:
                if self.run_address:
                    PC = self.run_address
                    self.run_address = None
                else:
                    self.running = 0
                combined.append('HLT')
                halt_code = instruction & 077
                if halt_code > 0:
                    print('halt code = %d' % halt_code)
            self.trace.itrace('+'.join(combined))
        return 1

    def page000(self, indirect, address, instruction):
        opcode = (instruction & 0177000) >> 9

        if opcode == 0000:
            if instruction & 0077700:
                self.illegal()
            return self.micro(instruction)
        elif opcode == 0001:
            return self.page001instructions.get(instruction, self.illegal)()
        elif opcode == 0002:
            return self.page002instructions.get(instruction, self.illegal)()
        elif opcode == 0003:
            shift = instruction & 3
            opcode = (instruction & 0777) >> 2
            return self.page003instructions.get(opcode, self.illegal)(shift)

    def page102(self, instruction):
        global PC

        if instruction == 0102001:
            if AC:
                PC = (PC + 1) & WORDMASK
            self.trace.itrace('ASN')
            return 1
        elif instruction == 0102002:
            if AC & HIGHBITMASK:
                PC = (PC + 1) & WORDMASK
            self.trace.itrace('ASM')
            return 1
        elif instruction == 0102004:
            if L:
                PC = (PC + 1) & WORDMASK
            self.trace.itrace('LSN')
            return 1
        elif instruction == 0102010:
            return self.i_DSN()
        elif instruction == 0102020:
            return self.i_KSN()
        elif instruction == 0102040:
            return self.i_RSN()
        elif instruction == 0102100:
            return self.i_TSN()
        elif instruction == 0102200:
            return self.i_SSN()
        elif instruction == 0102400:
            return self.i_HSN()
        else:
            self.illegal()
            

    def page100(self, indirect, address, instruction):
        opcode = (instruction & 0177000) >> 9

        if opcode == 0100:
            if ((instruction & 0077700) >> 6):
                self.illegal()
            return self.micro(instruction)
        elif opcode == 0102:
            return self.page102(instruction)
        else:
            self.illegal()


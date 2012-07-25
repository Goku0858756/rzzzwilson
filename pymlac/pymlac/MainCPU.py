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

        # main dispatch dictionary for decoding opcodes in bits 1-4
        self.main_decode = {000: self.page_00,	# secondary decode
                            001: self.i_LAW_LWC,
                            002: self.i_JMP,
#                            003: illegal,
                            004: self.i_DAC,
                            005: self.i_XAM,
                            006: self.i_ISZ,
                            007: self.i_JMS,
#                            010: illegal
                            011: self.i_AND,
                            012: self.i_IOR,
                            013: self.i_XOR,
                            014: self.i_LAC,
                            015: self.i_ADD,
                            016: self.i_SUB,
                            017: self.i_SAM}

        # page_00 dispatch dictionary for decoding opcodes
        # HLT may be handled specially
        self.page_00_decode = {001003: self.i_DLA,
                               001011: self.i_CTB,
                               001012: self.i_DOF,
                               001021: self.i_KRB,
                               001022: self.i_KCF,
                               001023: self.i_KRC,
                               001031: self.i_RRB,
                               001032: self.i_RCF,
                               001033: self.i_RRC,
                               001041: self.i_TPR,
                               001042: self.i_TCF,
                               001043: self.i_TPC,
                               001051: self.i_HRB,
                               001052: self.i_HOF,
                               001061: self.i_HON,
                               001062: self.i_STB,
                               001071: self.i_SCF,
                               001072: self.i_IOS,
                               001101: self.i_IOT101,
                               001111: self.i_IOT111,
                               001131: self.i_IOT131,
                               001132: self.i_IOT132,
                               001134: self.i_IOT134,
                               001141: self.i_IOT141,
                               001161: self.i_IOF,
                               001162: self.i_ION,
                               001271: self.i_PUN,
                               001274: self.i_PSF,
#                               003000: illegal RAL0
                               003001: self.i_RAL1,
                               003002: self.i_RAL2,
                               003003: self.i_RAL3,
#                               003020: illegal RAR0,
                               003021: self.i_RAR1,
                               003022: self.i_RAR2,
                               003023: self.i_RAR3,
#                               003040: illegal SAL0,
                               003041: self.i_SAL1,
                               003042: self.i_SAL2,
                               003043: self.i_SAL3,
#                               003060: illegal SAR0,
                               003061: self.i_SAR1,
                               003062: self.i_SAR2,
                               003063: self.i_SAR3,
                               003100: self.i_DON}

        self.page02_decode = {0002001: self.i_ASZ,
                              0102001: self.i_ASN,
                              0002002: self.i_ASP,
                              0102002: self.i_ASM,
                              0002004: self.i_LSZ,
                              0102004: self.i_LSN,
                              0002010: self.i_DSF,
                              0102010: self.i_DSN,
                              0002020: self.i_KSF,
                              0102020: self.i_KSN,
                              0002040: self.i_RSF,
                              0102040: self.i_RSN,
                              0002100: self.i_TSF,
                              0102100: self.i_TSN,
                              0002200: self.i_SSF,
                              0102200: self.i_SSN,
                              0002400: self.i_HSF,
                              0102400: self.i_HSN}


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

        # get instruction opcode, indirect bit and address
        opcode = (instruction >> 11) & 017
        indirect = (instruction & 0100000)
        address = (instruction & 03777)

        return self.main_decode.get(opcode, self.illegal)(indirect, address, instruction)

    def illegal(self, indirect, address, instruction=None):
        if instruction:
            msg = 'Illegal instruction (%6.6o) at address %6.6o' % (instruction, PC-1) 
        else:
            msg = 'Illegal instruction at address %6.6o' % (PC-1)
        raise RuntimeError(msg)

    def page_00(self, indirect, address, instruction):
        if (instruction & 0077700) == 000000:
            return self.microcode(instruction)
        elif (instruction & 0077000) == 002000:
            return self.page02_decode.get(instruction, self.illegal)()

        return self.page_00_decode.get(instruction, self.illegal)(indirect, address, instruction)

    def i_LAW_LWC(self, indirect, address, instruction):
        global AC

        if indirect:
            AC = ((~address) + 1) & WORDMASK
            self.trace.itrace('LWC', False, address)
        else:
            AC = address
            self.trace.itrace('LAW', False, address)
        return 1

    def i_JMP(self, indirect, address, instruction):
        global PC

        jmpaddr = self.EFFADDR(address)
        if indirect:
            jmpaddr = self.memory.get(jmpaddr, False)
        PC = jmpaddr & PCMASK
        self.trace.itrace('JMP', indirect, address)
        return 3 if indirect else 2

    def i_DAC(self, indirect, address, instruction):
        address = self.EFFADDR(address)
        self.memory.put(AC, address, indirect)
        self.trace.itrace('DAC', indirect, address)
        return 3 if indirect else 2

    def i_XAM(self, indirect, address, instruction):
        global AC

        if indirect:
            address = self.memory.get(address, False)
        tmp = self.memory.get(address, False)
        self.memory.put(AC, address, False)
        AC = tmp
        self.trace.itrace('XAM', indirect, address)
        return 3 if indirect else 2

    def i_ISZ(self, indirect, address, instruction):
        global PC

        value = (self.memory.get(address, indirect) + 1) & WORDMASK
        self.memory.put(value, address, False)
        if value == 0:
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('ISZ', indirect, address)
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

    def i_AND(self, indirect, address, instruction):
        global AC

        AC &= self.memory.get(address, indirect)
        self.trace.itrace('AND', indirect, address)
        return 3 if indirect else 2

    def i_IOR(self, indirect, address, instruction):
        global AC

        AC |= self.memory.get(address, indirect)
        self.trace.itrace('IOR', indirect, address)
        return 3 if indirect else 2

    def i_XOR(self, indirect, address, instruction):
        global AC

        AC ^= self.memory.get(address, indirect)
        self.trace.itrace('XOR', indirect, address)
        return 3 if indirect else 2

    def i_LAC(self, indirect, address, instruction):
        global AC

        AC = self.memory.get(address, indirect)
        self.trace.itrace('LAC', indirect, address)
        return 3 if indirect else 2

    def i_ADD(self, indirect, address, instruction):
        global AC, L

        effaddress = self.EFFADDR(address)
        AC += self.memory.get(address, indirect)
        if AC & OVERFLOWMASK:
            L = not L
            AC &= WORDMASK
        self.trace.itrace('ADD', indirect, address)
        return 3 if indirect else 2

    def i_SUB(self, indirect, address, instruction):
        global AC

        effaddr = self.EFFADDR(address)
        if indirect:
            effaddr = self.memory.get(effaddr, False)
        AC = (AC - self.memory.get(effaddr, False)) & WORDMASK
        self.trace.itrace('SUB', indirect, address)
        return 3 if indirect else 2

    def i_SAM(self, indirect, address, instruction):
        global PC

        samaddr = self.EFFADDR(address)
        if indirect:
            samaddr = self.memory.get(samaddr, False)
        if AC == self.memory.get(samaddr, False):
            PC = (PC + 1) & PCMASK
        self.trace.itrace('SAM', indirect, address)
        return 3 if indirect else 2

    def microcode(self, instruction):
        global AC, L

        # T1
        if (instruction & 001):
            AC = 0
           
        if (instruction & 010):
            L = 0

        # T2
        if (instruction & 002):
            AC = (~AC) & WORDMASK
        if (instruction & 020):
            L = (~L) & 1

        # T3
        if (instruction & 004):
            newac = AC + 1
            if newac & ~OVERFLOWMASK:
                L = (~L) & 1
            AC = newac & WORDMASK
        if (instruction & 040):
            AC |= self.dataswitches.read()
            L = (~L) & 1

        # do some sort of trace
        combined = []
        t = ''
        if instruction & 001:
            t = 'CLA'
        if instruction & 002:
            t = 'CMA'
        if (instruction & 003) == 03:
            t = 'STA'
        combined.append(t)
        t = ''
        if instruction & 010:
            t = 'CLL'
        if instruction & 020:
            t = 'CML'
        if (instruction & 030) == 030:
            t = 'STL'
        combined.append(t)
        if instruction & 004:
            combined.append('IAC')
        if instruction & 040:
            combined.append('ODA')

        self.trace.itrace('+'.join(combined), False)
        return 1

    def i_DLA(self, indirect, address, instruction):
        DisplayCPU.DPC = AC
        self.trace.itrace('DLA')
        return 1

    def i_CTB(self, indirect, address, instruction):
        self.trace.itrace('CTB')
        return 1

    def i_DOF(self, indirect, address, instruction):
        self.displaycpu.stop()
        self.trace.itrace('DOF')
        return 1

    def i_KRB(self, indirect, address, instruction):
        global AC

        AC |= self.kbd.read()
        self.trace.itrace('KRB')
        return 1

    def i_KCF(self, indirect, address, instruction):
        self.kbd.clear()
        self.trace.itrace('KCF')
        return 1

    def i_KRC(self, indirect, address, instruction):
        global AC

        AC |= self.kbd.read()
        self.kbd.clear()
        self.trace.itrace('KRC')
        return 1

    def i_RRB(self, indirect, address, instruction):
        global AC

        AC |= self.ttyin.read()
        self.trace.itrace('RRB')
        return 1

    def i_RCF(self, indirect, address, instruction):
        self.ttyin.clear()
        self.trace.itrace('RCF')
        return 1

    def i_RRC(self, indirect, address, instruction):
        global AC

        AC |= self.ttyin.read()
        self.ttyin.clear()
        self.trace.itrace('RRC')
        return 1

    def i_TPR(self, indirect, address, instruction):
        self.ttyout.write(AC & 0xff)
        self.trace.itrace('TPR')
        return 1

    def i_TCF(self, indirect, address, instruction):
        self.ttyout.clear()
        self.trace.itrace('TCF')
        return 1

    def i_TPC(self, indirect, address, instruction):
        self.ttyout.write(AC & 0xff)
        self.ttyout.clear()
        self.trace.itrace('TPC')
        return 1

    def i_HRB(self, indirect, address, instruction):
        global AC

        AC |= self.ptr.read()
        self.trace.itrace('HRB')
        return 1

    def i_HOF(self, indirect, address, instruction):
        self.ptr.stop()
        self.trace.itrace('HOF')
        return 1

    def i_HON(self, indirect, address, instruction):
        self.ptr.start()
        self.trace.itrace('HON')
        return 1

    def i_STB(self, indirect, address, instruction):
        self.trace.itrace('STB')
        return 1

    def i_SCF(self, indirect, address, instruction):
        global Sync40Hz

        Sync40Hz = 0
        self.trace.itrace('SCF')
        return 1

    def i_IOS(self, indirect, address, instruction):
        self.trace.itrace('IOS')
        return 1

    def i_IOT101(self, indirect, address, instruction):
        self.trace.itrace('IOT101')
        return 1

    def i_IOT111(self, indirect, address, instruction):
        self.trace.itrace('IOT111')
        return 1

    def i_IOT131(self, indirect, address, instruction):
        self.trace.itrace('IOT131')
        return 1

    def i_IOT132(self, indirect, address, instruction):
        self.trace.itrace('IOT132')
        return 1

    def i_IOT134(self, indirect, address, instruction):
        self.trace.itrace('IOT134')
        return 1

    def i_IOT141(self, indirect, address, instruction):
        self.trace.itrace('IOT141')
        return 1

    def i_IOF(self, indirect, address, instruction):
        self.trace.itrace('IOF')
        return 1

    def i_ION(self, indirect, address, instruction):
        self.trace.itrace('ION')
        return 1

    def i_PUN(self, indirect, address, instruction):
        self.ptp.write(PC & 0xff)
        self.trace.itrace('PUN')
        return 1

    def i_PSF(self, indirect, address, instruction):
        global PC

        if self.ptp.ready():
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('PSF')
        return 1

    def i_RAL1(self, indirect, address, instruction):
        global AC, L

        newl = AC >> 15
        newac = AC << 1 + L

        L = newl
        AC = newac & WORDMASK
        self.trace.itrace('RAL', 0, 1)
        return 1

    def i_RAL2(self, indirect, address, instruction):
        global AC, L

        highbits = AC >> 15
        newl = (AC >> 14) & 1
        newac = (((AC << 1) + L) << 1) + highbits

        L = newl
        AC = newac & WORDMASK
        self.trace.itrace('RAL', 0, 2)
        return 1

    def i_RAL3(self, indirect, address, instruction):
        global AC, L

        highbits = AC >> 14
        newl = (AC >> 13) & 1
        newac = (((AC << 1) + L) << 2) + highbits

        L = newl
        AC = newac & WORDMASK
        self.trace.itrace('RAL', 0, 3)
        return 1

    def i_RAR1(self, indirect, address, instruction):
        global AC, L

        newl = AC & 1
        newac = AC >> 1 + L << 15

        shift.regs.L = newl
        shift.regs.AC = newac & WORDMASK
        self.trace.itrace('RAR', 0, 1)
        return 1

    def i_RAR2(self, indirect, address, instruction):
        global AC, L

        lowbits = AC & 1
        newl = (AC >> 1) & 1
        newac = (((AC >> 1) + L << 15) >> 1) + lowbits << 15

        shift.regs.L = newl
        shift.regs.AC = newac & WORDMASK
        self.trace.itrace('RAR', 0, 2)
        return 1

    def i_RAR3(self, indirect, address, instruction):
        global AC, L

        lowbits = AC & 3
        newl = (AC >> 2) & 1
        newac = (((AC >> 1) + L << 15) >> 2) + lowbits << 14

        shift.regs.L = newl
        shift.regs.AC = newac & WORDMASK
        self.trace.itrace('RAR', 0, 3)
        return 1

    def i_SAL1(self, indirect, address, instruction):
        global AC

        AC = (AC << 1) & WORDMASK
        self.trace.itrace('SAL', 0, 1)
        return 1

    def i_SAL2(self, indirect, address, instruction):
        global AC

        AC = (AC << 2) & WORDMASK
        self.trace.itrace('SAL', 0, 2)
        return 1

    def i_SAL3(self, indirect, address, instruction):
        global AC

        AC = (AC << 3) & WORDMASK
        self.trace.itrace('SAL', 0, 3)
        return 1

    def i_SAR1(self, indirect, address, instruction):
        global AC

        AC >>= 1
        self.trace.itrace('SAR', 0, 1)
        return 1

    def i_SAR2(self, indirect, address, instruction):
        global AC

        AC >>= 2
        self.trace.itrace('SAR', 0, 2)
        return 1

    def i_SAR3(self, indirect, address, instruction):
        global AC

        AC >>= 3
        self.trace.itrace('SAR', 0, 3)
        return 1

    def i_DON(self, indirect, address, instruction):
        DisplayCPU.DRSindex = 0
        self.displaycpu.start()
        self.trace.itrace('DON')
        return 1

    def i_ASZ(self):
        global PC

        if AC == 0:
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('ASZ')
        return 1

    def i_ASN(self):
        global PC

        if AC != 0:
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('ASN')
        return 1

    def i_ASP(self):
        global PC

        if not (AC & HIGHBITMASK):
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('ASP')
        return 1

    def i_ASM(self):
        global PC

        if (AC & HIGHBITMASK):
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('ASM')
        return 1

    def i_LSZ(self):
        global PC

        if L == 0:
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('LSZ')
        return 1

    def i_LSN(self):
        global PC

        if L != 0:
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('LSN')
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


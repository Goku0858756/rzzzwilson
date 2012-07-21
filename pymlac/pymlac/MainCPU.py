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
#        self.dispatch = {000: self.page00,
#                         001: self.i_LAW,
#                         002: self.i_JMP,
#                         003: self.illegal,
#                         004: self.i_DAC,
#                         005: self.i_XAM,
#                         006: self.i_ISZ,
#                         007: self.i_JMS,
#                         010: self.illegal,
#                         011: self.i_AND,
#                         012: self.i_IOR,
#                         013: self.i_XOR,
#                         014: self.i_LAC,
#                         015: self.i_ADD,
#                         016: self.i_SUB,
#                         017: self.i_SAM,
#                         020: self.page20,
#                         021: self.i_LWC,
#                         022: self.i_JMP,
#                         023: self.illegal,
#                         024: self.i_DAC,
#                         025: self.i_XAM,
#                         026: self.i_ISZ,
#                         027: self.i_JMS,
#                         030: self.illegal,
#                         031: self.i_AND,
#                         032: self.i_IOR,
#                         033: self.i_XOR,
#                         034: self.i_LAC,
#                         035: self.i_ADD,
#                         036: self.i_SUB,
#                         037: self.i_SAM, }

    def EFFADDR(self, address):
        return BlockBase | address

    def execute_one_instruction(self):
        """Execute one MAIN instruction, return # cycles used"""

        global PC

        if not self.running:
            print('MainCPU halted')
            return 0

        global BlockBase

        # get instruction word to execute, advance PC
        instruction = self.memory.get(PC, False)
        BlockBase = PC & ADDRHIGHMASK
        PC = MASK_MEM(PC + 1)

        # break instruction into opcode and address
        indirect = instruction >> 15
        opcode = instruction >> 11
        address = instruction & 03777

#        return self.dispatch[opcode](indirect, address, instruction)

        if   opcode == 000:	return self.page00(indirect, address, instruction)
        elif opcode == 001:	return self.i_LAW(indirect, address, instruction)
        elif opcode == 002:	return self.i_JMP(indirect, address, instruction)
        elif opcode == 003:	return self.illegal(indirect, address, instruction)
        elif opcode == 004:	return self.i_DAC(indirect, address, instruction)
        elif opcode == 005:	return self.i_XAM(indirect, address, instruction)
        elif opcode == 006:	return self.i_ISZ(indirect, address, instruction)
        elif opcode == 007:	return self.i_JMS(indirect, address, instruction)
        elif opcode == 010:	return self.illegal(indirect, address, instruction)
        elif opcode == 011:	return self.i_AND(indirect, address, instruction)
        elif opcode == 012:	return self.i_IOR(indirect, address, instruction)
        elif opcode == 013:	return self.i_XOR(indirect, address, instruction)
        elif opcode == 014:	return self.i_LAC(indirect, address, instruction)
        elif opcode == 015:	return self.i_ADD(indirect, address, instruction)
        elif opcode == 016:	return self.i_SUB(indirect, address, instruction)
        elif opcode == 017:	return self.i_SAM(indirect, address, instruction)
        elif opcode == 020:	return self.page20(indirect, address, instruction)
        elif opcode == 021:	return self.i_LWC(indirect, address, instruction)
        elif opcode == 022:	return self.i_JMP(indirect, address, instruction)
        elif opcode == 023:	return self.illegal(indirect, address, instruction)
        elif opcode == 024:	return self.i_DAC(indirect, address, instruction)
        elif opcode == 025:	return self.i_XAM(indirect, address, instruction)
        elif opcode == 026:	return self.i_ISZ(indirect, address, instruction)
        elif opcode == 027:	return self.i_JMS(indirect, address, instruction)
        elif opcode == 030:	return self.illegal(indirect, address, instruction)
        elif opcode == 031:	return self.i_AND(indirect, address, instruction)
        elif opcode == 032:	return self.i_IOR(indirect, address, instruction)
        elif opcode == 033:	return self.i_XOR(indirect, address, instruction)
        elif opcode == 034:	return self.i_LAC(indirect, address, instruction)
        elif opcode == 035:	return self.i_ADD(indirect, address, instruction)
        elif opcode == 036:	return self.i_SUB(indirect, address, instruction)
        elif opcode == 037:	return self.i_SAM(indirect, address, instruction)

    def illegal(self, indirect, address, instruction=None):
        if instruction:
            print 'Illegal instruction (', '%6.6o' % instruction,') at address ', '%6.6o' % (PC-1)
        else:
            print 'Illegal instruction at address', '%6.6o' % (PC-1)
        sys.exit(0)

    def i_ADD(self, indirect, address, instruction):
        global AC, L

        cycles = 3 if indirect else 2
        effaddress = self.EFFADDR(address)
        AC += self.memory.get(address, indirect)
        if AC & OVERFLOWMASK:
            L = not L
            AC &= WORDMASK
        self.trace.itrace('ADD', indirect, address)
        return cycles

    def i_AND(self, indirect, address, instruction):
        global AC

        cycles = 3 if indirect else 2
        AC &= self.memory.get(address, indirect)
        self.trace.itrace('AND', indirect, address)
        return cycles

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
        cycles = 3 if indirect else 2

        address = self.EFFADDR(address)
        self.memory.put(AC, address, indirect)
        self.trace.itrace('DAC', indirect, address)
        return cycles

    def i_DLA(self):
        DisplayCPU.DPC = AC
        self.trace.itrace('DLA')
        return 1

    def i_DOF(self):
        self.displaycpu.stop()
        self.trace.itrace('DOF')
        return 1

    def i_DON(self):
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

        cycles = 3 if indirect else 2

        AC |= self.memory.get(address, indirect)
        self.trace.itrace('IOR', indirect, address)
        return cycles

    def i_IOS(self):
        self.trace.itrace('IOS')
        return 1

    def i_ISZ(self, indirect, address, instruction):
        global PC

        cycles = 3 if indirect else 2

        value = (self.memory.get(address, indirect) + 1) & WORDMASK
        self.memory.put(value, address, False)
        if value == 0:
            PC = (PC + 1) & WORDMASK
        self.trace.itrace('ISZ', indirect, address)
        return cycles

    def i_JMP(self, indirect, address, instruction):
        global PC

        cycles = 3 if indirect else 2

        jmpaddr = self.EFFADDR(address)
        if indirect:
            jmpaddr = self.memory.get(jmpaddr, False)
        PC = jmpaddr & PCMASK

        self.trace.itrace('JMP', indirect, address)
        return cycles

    def i_JMS(self, indirect, address, instruction):
        global PC

        cycles = 3 if indirect else 2
        jmsaddr = self.EFFADDR(address)
        if indirect:
            jmsaddr = self.memory.get(jmsaddr, False)
        self.memory.put(PC, jmsaddr, False)
        PC = (jmsaddr + 1) & PCMASK
        self.trace.itrace('JMS', indirect, address)
        return cycles

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

        cycles = 3 if indirect else 2
        AC = self.memory.get(address, indirect)
        self.trace.itrace('LAC', indirect, address)
        return cycles

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

        cycles = 3 if indirect else 2
        samaddr = self.EFFADDR(address)
        if indirect:
            samaddr = self.memory.get(samaddr, False)
        if AC == self.memory.get(samaddr, False):
            PC = (PC + 1) & PCMASK
        self.trace.itrace('SAM', indirect, address)
        return cycles

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

        cycles = 3 if indirect else 2
        effaddr = self.EFFADDR(address)
        if indirect:
            effaddr = self.memory.get(effaddr, False)
        AC = (AC - self.memory.get(effaddr, False)) & WORDMASK
        self.trace.itrace('SUB', indirect, address)
        return cycles

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

        cycles = 3 if indirect else 2
        if indirect:
            address = self.memory.get(address, False)
        tmp = self.memory.get(address, False)
        self.memory.put(AC, address, False)
        AC = tmp
        self.trace.itrace('XAM', indirect, address)
        return cycles

    def i_XOR(self, indirect, address, instruction):
        global AC

        cycles = 3 if indirect else 2
        AC ^= self.memory.get(address, indirect)
        self.trace.itrace('XOR', indirect, address)
        return cycles

    # this is fiddly because we want to trace the single operation opcoded instructions
    # *and* the encoded multiple non-opcoded instructions sensibly.
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
            notfirst = 0
            if instruction & 000001:
                AC = 0
                self.trace.trace('CLA'); notfirst = 1
            if instruction & 000010:
                L = 0
                if notfirst: self.trace.trace('+')
                self.trace.trace('CLL'); notfirst = 1
            if instruction & 000002:
                AC = (~AC) & WORDMASK
                if notfirst: self.trace.trace('+')
                self.trace.trace('CMA'); notfirst = 1
            if instruction & 000020:
                L = (~L) & 1
                if notfirst: self.trace.trace('+')
                self.trace.trace('CMA'); notfirst = 1
            if instruction & 000004:
                newac = AC + 1
                if newac & OVERFLOWMASK:
                    L = not L
                AC = newac & WORDMASK
                if notfirst: self.trace.trace('+')
                self.trace.trace('IAC'); notfirst = 1
            if instruction & 000040:
                AC |= self.dataswitches.read()
                if notfirst: self.trace.trace('+')
                self.trace.trace('ODA'); notfirst = 1
            if (instruction & 0100000) == 0:
                if self.run_address:
                    PC = self.run_address
                    self.run_address = None
                else:
                    self.running = 0
                if notfirst: self.trace.trace('+')
                self.trace.itrace('HLT'); notfirst = 1
        return 1

    def page00(self, indirect, address, instruction):
        opcode = (instruction & 0177000) >> 9

        if opcode == 0000:
            if ((instruction & 0077700) >> 6):
                self.illegal()
            return self.micro(instruction)
        elif opcode == 0001:
            return self.page001(instruction)
        elif opcode == 0002:
            return self.page002(instruction)
        elif opcode == 0003:
            return self.page003(instruction)

    def page001(self, instruction):
        if instruction == 0001003:
            return self.i_DLA()
        elif instruction == 0001011:
            self.illegal(instruction)	# CTB
        elif instruction == 0001012:
            return self.i_DOF()
        elif instruction == 0001021:
            return self.i_KRB()
        elif instruction == 0001022:
            return self.i_KCF()
        elif instruction == 0001023:
            return self.i_KRC()
        elif instruction == 0001031:
            return self.i_RRB()
        elif instruction == 0001032:
            return self.i_RCF()
        elif instruction == 0001033:
            return self.i_RRC()
        elif instruction == 0001041:
            return self.i_TPR()
        elif instruction == 0001042:
            return self.i_TCF()
        elif instruction == 0001043:
            return self.i_TPC()
        elif instruction == 0001051:
            return self.i_HRB()
        elif instruction == 0001052:
            return self.i_HOF()
        elif instruction == 0001061:
            return self.i_HON()
        elif instruction == 0001071:
            return self.i_SCF()
        elif instruction == 0001072:
            return self.i_IOS()
        elif instruction == 0001101:
            self.illegal(instruction)	# IOT 101
        elif instruction == 0001111:
            self.illegal(instruction)	# IOT 111
        elif instruction == 0001131:
            self.illegal(instruction)	# IOT 131
        elif instruction == 0001132:
            self.illegal(instruction)	# IOT 132
        elif instruction == 0001134:
            self.illegal(instruction)	# IOT 134
        elif instruction == 0001141:
            self.illegal(instruction)	# IOT 141
        elif instruction == 0001161:
            self.illegal(instruction)	# IOT 161
        elif instruction == 0001162:
            self.illegal(instruction)	# IOT 162
        elif instruction == 0001271:
            return self.i_PUN()
        elif instruction == 0001274:
            return self.i_PSF()
        else:
            self.illegal(instruction)

    def page002(self, instruction):
        if instruction == 0002001:
            return self.i_ASZ()
        if instruction == 0002002:
            return self.i_ASP()
        if instruction == 0002004:
            return self.i_LSZ()
        if instruction == 0002010:
            return self.i_DSF()
        if instruction == 0002020:
            return self.i_KSF()
        if instruction == 0002040:
            return self.i_RSF()
        if instruction == 0002100:
            return self.i_TSF()
        if instruction == 0002200:
            return self.i_SSF()
        if instruction == 0002400:
            return self.i_HSF()
        self.illegal(instruction)

    def page003(self, instruction):
        shift = instruction & 3
        opcode = (instruction & 0777) >> 2
        if opcode == 000:
            return self.i_RAL(shift)
        elif opcode == 004:
            return self.i_RAR(shift)
        elif opcode == 010:
            return self.i_SAL(shift)
        elif opcode == 014:
            return self.i_SAR(shift)
        elif opcode == 020:
            return self.i_DON()
        else:
            self.illegal(instruction)

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
            

    def page20(self, indirect, address, instruction):
        opcode = (instruction & 0177000) >> 9

        if opcode == 0100:
            if ((instruction & 0077700) >> 6):
                self.illegal()
            return self.micro(instruction)
        elif opcode == 0102:
            return self.page102(instruction)
        else:
            self.illegal()


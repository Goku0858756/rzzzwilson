#!/usr/bin/python 

"""
Class to emulate the Imlac Memory.
"""


import pickle

import Globals
from Globals import *


class Memory(object):
    ROM_START = 040
    ROM_SIZE = 040

    # this PTR bootstrap from "Loading The PDS-1" (loading.pdf)
    PTR_ROM_IMAGE = [ 0060077, # start  lac    base  ;40 get load address
                      0020010, #        dac    10    ;41 put into auto-inc reg
                      0104076, #        lwc    0080  ;42 -080 into AC
                      0020020, #        dac    20    ;43 put into memory
                      0001061, #        hon          ;44 start PTR
                      0100011, # wait   cal          ;45 clear AC+LINK
                      0002400, #        hsf          ;46 skip if PTR has data
                      0010046, #        jmp    .-1   ;47 wait until is data
                      0001051, #        hrb          ;50 read PTR -> AC
                      0074075, #        sam    what  ;51 skip if AC == 2
                      0010045, #        jmp    wait  ;52 wait until PTR return 0
                      0002400, # loop   hsf          ;53 skip if PTR has data
                      0010053, #        jmp    .-1   ;54 wait until is data
                      0001051, #        hrb          ;55 read PTR -> AC
                      0003003, #        ral    3     ;56 move byte into high AC
                      0003003, #        ral    3     ;57
                      0003002, #        ral    2     ;60
                      0102400, #        hsn          ;61 wait until PTR moves
                      0010061, #        jmp    .-1   ;62
                      0002400, #        hsf          ;63 skip if PTR has data
                      0010063, #        jmp    .-1   ;64 wait until is data
                      0001051, #        hrb          ;65 read PTR -> AC
                      0120010, #        dac    *10   ;66 store word, inc pointer
                      0102400, #        hsn          ;67 wait until PTR moves
                      0010067, #        jmp    .-1   ;70
                      0100011, #        cal          ;71 clear AC & LINK
                      0030020, #        isz    20    ;72 inc mem and skip zero
                      0010053, #        jmp    loop  ;73 if not finished, jump
                      0110076, #        jmp    *go   ;74 execute loader
                      0000002, # what   data   2     ;75
                      0003700, # go     word   03700H;76
                      0003677  # base   word   03677H;77
                    ]
    TTY_ROM_IMAGE = [ 0060077, # start  lac    base   ;40 get load address
                      0020010, #        dac    10     ;41 put into auto-inc reg
                      0104076, #        lwc    076    ;42 -076 into AC (loader size)
                      0020020, #        dac    20     ;43 put into memory
                      0001032, #        rcf           ;44 clear TTY flag
                      0100011, # wait   cal           ;45 clear AC+LINK
                      0002040, #        rsf           ;46 skip if TTY has data
                      0010046, #        jmp    .-1    ;47 wait until there is data
                      0001031, #        rrb           ;50 read TTY -> AC
                      0074075, #        sam    75     ;51 first non-zero must be 02
                      0010044, #        jmp    044    ;52 wait until TTY return == 02
                      0002040, # loop   rsf           ;53 skip if TTY has data
                      0010053, #        jmp    .-1    ;54 wait until there is data
                      0001033, #        rrc           ;55 read TTY -> AC
                      0003003, #        ral    3      ;56 move TTY byte into high AC
                      0003003, #        ral    3      ;57
                      0003002, #        ral    2      ;60
                      0002040, #        rsf           ;61 wait until there is data
                      0010061, #        jmp    .-1    ;62
                      0001033, #        rrc           ;63 read TTY -> AC, clear flag
                      0120010, #        dac    *10    ;64 store word, inc pointer
                      0100011, #        cal           ;65 clear AC & LINK
                      0030020, #        isz    20     ;66 inc mem and skip if zero
                      0010053, #        jmp    loop   ;67 if not finished, next word
                      0110076, #        jmp    *go    ;70 else execute block loader
                      0000000, #        hlt           ;71
                      0000000, #        hlt           ;72
                      0000000, #        hlt           ;73
                      0000000, #        hlt           ;74
                      0000002, #        data   2      ;75
                      0037700, # go     word   037700 ;76 block loader base address
                      0037677  # base   word   037677 ;77 init value for 010 auto inc
                    ]

    def __init__(self, boot_rom=ROM_PTR, corefile=None):
        self.memory = []
        if corefile:
            try:
                self.loadcore(corefile)
            except IOError:
                self.__init_core()
        else:
            self.__init_core()
        
        if boot_rom == ROM_PTR:
            self.set_PTR_ROM()
        else:
            self.set_TTY_ROM()

    def __init_core(self):
        for i in range(MEMORY_SIZE):
            self.memory.append(0)

    def loadcore(self, file=None):
        if file:
            filed = open(file, 'r')
            self.memory = pickle.load(filed)
            filed.close()

    def savecore(self, file=None):
        if file:
            try:
                filed = open(file, 'w')
                pickle.dump(self.memory, filed)
                filed.close()
            except IOError:
                pass

    def set_PTR_ROM(self):
        i = self.ROM_START
        count = 0
        while count < self.ROM_SIZE:
            self.memory[i] = self.PTR_ROM_IMAGE[count]
            i += 1
            count += 1

    def set_TTY_ROM(self):
        i = self.ROM_START
        count = 0
        while count < self.ROM_SIZE:
            self.memory[i] = self.TTY_ROM_IMAGE[count]
            i += 1
            count += 1

    def get(self, address, indirect):
        if indirect:
            if ISAUTOINC(address):
                self.memory[address] = MASK_MEM(self.memory[address] + 1)
            address = self.memory[address]
        return self.memory[address]

    def put(self, value, address, indirect):
        if indirect:
            if ISAUTOINC(address):
                self.memory[address] = MASK_MEM(self.memory[address] + 1)
            address = self.memory[address] & ADDRMASK
        try:
            self.memory[address] = MASK_16(value)
        except IndexError:
            print('Bad address: %06o (max mem=%06o, ADDRMASK=%06o)' % (address, len(self.memory), ADDRMASK))
            raise

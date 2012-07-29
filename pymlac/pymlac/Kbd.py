#!/usr/bin/python 

"""
Class to emulate the Keyboard (KBD).

We must emulate funny Imlac key values.
"""


#import pygame
#from pygame.locals import *


######
# This string has a \000 char at the PC key ordinal position if the key is dead.
# Anything else and the key is live and the value is the unshifted value.
######

#            0   1   2   3   4   5   6   7   8   9   A   B   C   D   E   F
keyval = ('\000\000\000\000\000\000\000\000\000\211\000\000\000\215\000\000' #00
          '\000\000\000\231\000\000\000\000\000\000\000\233\000\000\000\000' #01
          '\240\000\000\000\000\000\000\247\000\000\000\000\254\255\256\257' #02
          '\260\261\262\263\264\265\266\267\270\271\000\273\000\275\000\000' #03
          '\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000' #04
          '\000\000\000\000\000\000\000\000\000\000\000\000\212\000\000\000' #05
          '\000\341\342\343\344\345\346\347\350\351\352\353\354\355\356\357' #06
          '\360\361\362\363\364\365\366\367\370\371\372\000\000\000\000\377' #07
          '\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000' #08
          '\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000' #09
          '\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000' #0A
          '\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000' #0B
          '\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000' #0C
          '\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000' #0D
          '\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000' #0E
          '\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000' #0F
          '\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000' #10
          '\000\206\204\205\210\202\217\216\000\214\000\000\000\000\000\000' #11
          '\000\000\000\000\000\000\000\000\000\000\000\000\000')            #12

######
# This string has the shifted values for the key, indexed by PC key number.
######

#             0   1   2   3   4   5   6   7   8   9   A   B   C   D   E   F
skeyval = ('\000\000\000\000\000\000\000\000\000\211\000\000\000\215\000\000'#00
           '\000\000\000\231\000\000\000\000\000\000\000\233\000\000\000\000'#01
           '\240\000\000\000\000\000\000\242\000\000\000\000\274\255\276\277'#02
           '\251\241\262\243\244\245\266\246\252\250\000\272\000\253\000\000'#03
           '\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000'#04
           '\000\000\000\000\000\000\000\000\000\000\000\000\212\000\000\000'#05
           '\000\301\302\303\304\305\306\307\310\311\312\313\314\315\316\317'#06
           '\320\321\322\323\324\325\326\327\330\331\332\000\000\000\000\377'#07
           '\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000'#08
           '\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000'#09
           '\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000'#0A
           '\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000'#0B
           '\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000'#0C
           '\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000'#0D
           '\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000'#0E
           '\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000'#0F
           '\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000'#10
           '\000\206\204\205\210\202\217\216\000\214\000\000\000\000\000\000'#11
           '\000\000\000\000\000\000\000\000\000\000\000\000\000')           #12


class Kbd(object):
    def init(self):
        self.value = 0
        self.clear()

    def handle_events(self):
        pass
#        for event in pygame.event.get():
#            if (event.type == KEYDOWN):
#                if (event.key < 300) and ord(keyval[event.key]) != 0:
#                    self.value = ord(keyval[event.key])
#                    if (event.mod & 0x03 or event.mod & 0x2000):	# handle SHIFT
#                        self.value = ord(skeyval[event.key]) | 0x0100
#                    if (event.mod & 0x00C0):				# handle CONTROL
#                        self.value = self.value | 0x0200
#                    if (event.mod & 0x0300):				# handle REPEAT
#                        self.value = self.value | 0x0400
#                    self.ready = 1
#                    return

    def is_ready(self):
        return self.ready

    def clear(self):
        self.ready = 0

    def read(self):
        return self.value


def test_main():
    """ Test the emulation of the KBD device """
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('pymlac KBD emulation')

    kbd = Kbd()
    kbd.clear()
    while (1):
        kbd.handle_events()
        if (kbd.is_ready()):
            print oct(kbd.read())
            kbd.clear()


if __name__ == '__main__':
    test_main()

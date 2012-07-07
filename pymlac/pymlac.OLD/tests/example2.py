#!/usr/bin/python
########################################################################################################
# For handling filenames... 
import os, time, sys

# The pygame module itself...
import pygame

# The image handling...
import pygame.image

# Important constant definitions for Pygame, 
# in this example: used to setup the "Double Buffered" Display...
from pygame.locals import *

# Initialise SDL environment
pygame.init()        

# Get the image from: ./images/pygamelogo1.gif
#panel_file = os.path.join('images', 'panel.png')
#led_on_file = os.path.join('images', 'led_on.png')
#led_off_file = os.path.join('images', 'led_off.png')

ITEM_HEIGHT = 17
DEVICEMENU = ('Mount', 'Dismount', 'Rewind', 'Turn on', 'Turn off')

snapshot_file = 'pymlac_snap.bmp'

BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,64)
GREY = (128,128,128)
LIGHTGREY = (182,182,182)
RED = (128, 0, 0)

VERSION_POSN = (173,0)

CANVAS_WIDTH = 1024
CANVAS_HEIGHT = 1024

BOX_POSNX = 5
BOX_POSNY = 45
BOX_OFFSETY = 42
BOX_WIDTH = 246
BOX_HEIGHT = 20
LABEL_OFFSETY = -19
EOF_OFFSETX = CANVAS_WIDTH + BOX_POSNX + 180
TAGS_OFFSETY = -17
ON_OFFSETX = 1254
OFF_OFFSETX = 1247
FILE_OFSETX = 1032
FILE_OFFSETY = +1

PTR_BOX_POSNY = BOX_POSNY
PTR_LABEL_POSN = (BOX_POSNX, PTR_BOX_POSNY + LABEL_OFFSETY)
PTR_EOF_POSN = (EOF_OFFSETX, PTR_BOX_POSNY + TAGS_OFFSETY)
PTR_ON_POSN = (ON_OFFSETX, PTR_BOX_POSNY + TAGS_OFFSETY)
PTR_OFF_POSN = (OFF_OFFSETX, PTR_BOX_POSNY + TAGS_OFFSETY)
PTR_FILE_POSN = (FILE_OFSETX, PTR_BOX_POSNY + FILE_OFFSETY)

PTP_BOX_POSNY = PTR_BOX_POSNY + BOX_OFFSETY
PTP_LABEL_POSN = (BOX_POSNX, PTP_BOX_POSNY + LABEL_OFFSETY)
PTP_EOF_POSN = (EOF_OFFSETX, PTP_BOX_POSNY + TAGS_OFFSETY)
PTP_ON_POSN = (ON_OFFSETX, PTP_BOX_POSNY + TAGS_OFFSETY)
PTP_OFF_POSN = (OFF_OFFSETX, PTP_BOX_POSNY + TAGS_OFFSETY)
PTP_FILE_POSN = (FILE_OFSETX, PTP_BOX_POSNY + FILE_OFFSETY)

TTYIN_BOX_POSNY = PTP_BOX_POSNY + BOX_OFFSETY
TTYIN_LABEL_POSN = (BOX_POSNX, TTYIN_BOX_POSNY + LABEL_OFFSETY)
TTYIN_EOF_POSN = (EOF_OFFSETX, TTYIN_BOX_POSNY + TAGS_OFFSETY)
TTYIN_ON_POSN = (ON_OFFSETX, TTYIN_BOX_POSNY + TAGS_OFFSETY)
TTYIN_OFF_POSN = (OFF_OFFSETX, TTYIN_BOX_POSNY + TAGS_OFFSETY)
TTYIN_FILE_POSN = (FILE_OFSETX, TTYIN_BOX_POSNY + FILE_OFFSETY)

TTYOUT_BOX_POSNY = TTYIN_BOX_POSNY + BOX_OFFSETY
TTYOUT_LABEL_POSN = (BOX_POSNX, TTYOUT_BOX_POSNY + LABEL_OFFSETY)
TTYOUT_EOF_POSN = (EOF_OFFSETX, TTYOUT_BOX_POSNY + TAGS_OFFSETY)
TTYOUT_ON_POSN = (ON_OFFSETX, TTYOUT_BOX_POSNY + TAGS_OFFSETY)
TTYOUT_OFF_POSN = (OFF_OFFSETX, TTYOUT_BOX_POSNY + TAGS_OFFSETY)
TTYOUT_FILE_POSN = (FILE_OFSETX, TTYOUT_BOX_POSNY + FILE_OFFSETY)

LEDAC_LABEL_OFFSETY = -18
LEDL_POSNX = 0
LEDAC_POSNX = 17
LEDAC_POSNY = 715
LEDPC_LABEL_OFFSETY = -18
LEDPC_POSNX = 17
LEDPC_POSNY = LEDAC_POSNY + 35
LED_BIT_OFFSETX = 15
LED_BIT_RANGE = (15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0)

LEDL_SCREEN_POSNX = CANVAS_WIDTH + LEDL_POSNX
LEDAC_SCREEN_POSNX = CANVAS_WIDTH + LEDAC_POSNX
LEDAC_SCREEN_POSNY = LEDAC_POSNY

LEDPC_SCREEN_POSNX = CANVAS_WIDTH + LEDPC_POSNX
LEDPC_SCREEN_POSNY = LEDPC_POSNY

PANEL_WIDTH = 256

REGS_MON_DIVIDERY = 205
ROM_MON_DIVIDERY = 285
FILE_ROM_DIVIDER = 690
MON_LED_DIVIDERY = 775
BOX_BOT_DIVIDERY = 875

BOX_POSNY = 802

REGL_BOX_POSNX = 73
REGL_BOX_POSNY = BOX_POSNY
REGL_BOX_WIDTH = 15
REGL_BOX_HEIGHT = 20

REGAC_BOX_POSNX = 95
REGAC_BOX_POSNY = REGL_BOX_POSNY
REGAC_BOX_WIDTH = 55
REGAC_BOX_HEIGHT = 20

REGPC_BOX_POSNX = 170
REGPC_BOX_POSNY = REGL_BOX_POSNY
REGPC_BOX_WIDTH = 55
REGPC_BOX_HEIGHT = 20

REGDX_BOX_POSNX = 33
REGDX_BOX_POSNY = BOX_POSNY + 40
REGDX_BOX_WIDTH = 55
REGDX_BOX_HEIGHT = 20

REGDY_BOX_POSNX = 95
REGDY_BOX_POSNY = REGDX_BOX_POSNY
REGDY_BOX_WIDTH = 55
REGDY_BOX_HEIGHT = 20

REGDPC_BOX_POSNX = 170
REGDPC_BOX_POSNY = REGDX_BOX_POSNY
REGDPC_BOX_WIDTH = 55
REGDPC_BOX_HEIGHT = 20

BOX_DATA_OFFSETX = 4
BOX_DATA_OFFSETY = 2

BOOTROM_POSNX = 10
BOOTROM_POSNY = 215

BOOTROM_LABEL_POSN = (BOOTROM_POSNX, BOOTROM_POSNY)
BOOTROM_LOADPTR_RADIO_POSN = (BOOTROM_POSNX + 5, BOOTROM_POSNY + 20)
BOOTROM_LOADPTR_LABEL_POSN = (BOOTROM_POSNX + 28, BOOTROM_POSNY + 18)
BOOTROM_LOADTTY_RADIO_POSN = (BOOTROM_POSNX + 5, BOOTROM_POSNY + 40)
BOOTROM_LOADTTY_LABEL_POSN = (BOOTROM_POSNX + 28, BOOTROM_POSNY + 40)
BOOTROM_WRITABLE_POSN = (BOOTROM_POSNX + 125, BOOTROM_POSNY + 20)
BOOTROM_WRITABLE_LABEL_POSN = (BOOTROM_POSNX + 148, BOOTROM_POSNY + 18)

SCREEN_BOOTROM_WRITABLE_POSN = (CANVAS_WIDTH + BOOTROM_POSNX + 125, BOOTROM_POSNY + 20)
SCREEN_BOOTROM_LOADPTR_RADIO_POSN = (CANVAS_WIDTH + BOOTROM_POSNX + 5, BOOTROM_POSNY + 20)
SCREEN_BOOTROM_LOADTTY_RADIO_POSN = (CANVAS_WIDTH + BOOTROM_POSNX + 5, BOOTROM_POSNY + 40) 


QUITBUTTON_POSN = (142, 930)
HALTBUTTON_POSN = (14, 930)
RUNBUTTON_POSN = HALTBUTTON_POSN
SINGLESTEPBUTTON_POSN = (14, 890)

SCREEN_QUITBUTTON_POSN = (CANVAS_WIDTH + 142, 930)
SCREEN_HALTBUTTON_POSN = (CANVAS_WIDTH + 14, 930)
SCREEN_SINGLESTEPBUTTON_POSN = (CANVAS_WIDTH + 14, 890)

HALT_RECT = (SCREEN_HALTBUTTON_POSN, (100, 25))
QUIT_RECT = (SCREEN_QUITBUTTON_POSN, (100, 25))
SINGLESTEP_RECT = (SCREEN_SINGLESTEPBUTTON_POSN, (228, 25))
ROM_WRITABLE_RECT = (SCREEN_BOOTROM_WRITABLE_POSN, (19, 19))
LOADPTR_RADIO_RECT = (SCREEN_BOOTROM_LOADPTR_RADIO_POSN, (19, 19))
LOADTTY_RADIO_RECT = (SCREEN_BOOTROM_LOADTTY_RADIO_POSN, (19, 19))

quit_rect = pygame.Rect(QUIT_RECT)
halt_rect = pygame.Rect(HALT_RECT)
singlestep_rect = pygame.Rect(SINGLESTEP_RECT)
romwritable_rect = pygame.Rect(ROM_WRITABLE_RECT)
loadptrradio_rect = pygame.Rect(LOADPTR_RADIO_RECT)
loadttyradio_rect = pygame.Rect(LOADTTY_RADIO_RECT)
ptrfilename_rect = pygame.Rect(PTR_FILE_POSN, (BOX_WIDTH, BOX_HEIGHT))
ptpfilename_rect = pygame.Rect(PTP_FILE_POSN, (BOX_WIDTH, BOX_HEIGHT))
ttyinfilename_rect = pygame.Rect(TTYIN_FILE_POSN, (BOX_WIDTH, BOX_HEIGHT))
ttyoutfilename_rect = pygame.Rect(TTYOUT_FILE_POSN, (BOX_WIDTH, BOX_HEIGHT))

font_data = pygame.font.Font(None, 21)
font_label = pygame.font.Font(None, 24)

checkbox_on = pygame.image.load(os.path.join('images', 'checkon.png'))
checkbox_off = pygame.image.load(os.path.join('images', 'checkoff.png'))
radiobutton_on = pygame.image.load(os.path.join('images', 'radioon.png'))
radiobutton_off = pygame.image.load(os.path.join('images', 'radiooff.png'))

class Menu:
    def __init__(self, itemlist, width):
        self.itemlist = itemlist
        self.numitems = len(itemlist)
        self.height = self.numitems * ITEM_HEIGHT # + ITEM_HEIGHT / 3
        self.width = width
        self.beforesurface = pygame.Surface((self.width, self.width))
        self.menusurface = pygame.Surface((self.width, self.height))
        self.menusurface.fill(BLACK)
        self.menusurface.fill(WHITE, ((1, 1), (self.width - 2, self.height - 2)))
        offset = 0
        for item in itemlist:
            self.menusurface.blit(font_data.render('%s' % item, 1, RED), (5, offset))
            offset += ITEM_HEIGHT

    def show(self, display, posn):
        x, y = posn
        if (x > display.get_width() - self.width):
            newposn = (x - self.width, y)
        else:
            newposn = posn

        menurect = pygame.Rect(newposn, (self.width, self.height))
        sourcerect = (newposn, (self.width, self.height))
        self.beforesurface.blit(display, (0, 0), sourcerect)
        display.blit(self.menusurface, newposn)
        pygame.display.flip()
        result = 0
        end_flag = 1
        while end_flag:
            pygame.event.pump()
            for event in pygame.event.get():
                if (event.type == MOUSEBUTTONUP):
                    if (event.button == 1):
                        if (menurect.collidepoint(event.pos)):
                            display.blit(self.beforesurface, newposn)
                            pygame.display.flip()
                            x, y = newposn
                            result = (event.pos[1] - y) / ITEM_HEIGHT + 1
                            if (result > self.numitems):
                                result = self.numitems
                        end_flag = 0
        display.blit(self.beforesurface, newposn)
        pygame.display.flip()
        return result
       

def draw_checkbox(surface, posn, on):
    if (on):
        surface.blit(checkbox_on, posn)
    else:
        surface.blit(checkbox_off, posn)

def draw_radiobutton(surface, posn, on):
    if (on):
        surface.blit(radiobutton_on, posn)
    else:
        surface.blit(radiobutton_off, posn)

def update_octalbox(surface, x, y, format, value):
    surface.blit(font_data.render(format % value, 1, BLACK), (x + BOX_DATA_OFFSETX, y + BOX_DATA_OFFSETY))

def draw_divider(surface, y, width):
    pygame.draw.line(surface, LIGHTGREY, (0, y), (width - 1, y))
    pygame.draw.line(surface, BLACK, (0, y+1), (width - 1, y+1))

def draw_databox(surface, label, x, y, width, height):
    if (len(label) > 0):
        surface.blit(font_label.render(label, 1, BLACK), (x, y + LABEL_OFFSETY))
    pygame.draw.rect(surface, BLACK, ((x, y), (width, height)), 1)
    surface.fill(WHITE, ((x + 1,y + 1),(width - 2,height - 2)))

def panel_init(panel, led_on, led_off, halt, quit, ss):
    panel.blit(font_label.render('pymlac 0.1', 1, BLACK), VERSION_POSN)

    draw_databox(panel, 'ptr', BOX_POSNX, PTR_BOX_POSNY, BOX_WIDTH, BOX_HEIGHT)
    draw_databox(panel, 'ptp', BOX_POSNX, PTP_BOX_POSNY, BOX_WIDTH, BOX_HEIGHT)
    draw_databox(panel, 'ttyin', BOX_POSNX, TTYIN_BOX_POSNY, BOX_WIDTH, BOX_HEIGHT)
    draw_databox(panel, 'ttyout', BOX_POSNX, TTYOUT_BOX_POSNY, BOX_WIDTH, BOX_HEIGHT)

    panel.blit(led_off, (LEDL_POSNX, LEDAC_POSNY))
    panel.blit(font_label.render('l', 1, BLACK), (LEDL_POSNX, LEDAC_POSNY + LEDAC_LABEL_OFFSETY))
    panel.blit(font_label.render('ac', 1, BLACK), (LEDAC_POSNX, LEDAC_POSNY + LEDAC_LABEL_OFFSETY))
    led_posnx = LEDAC_POSNX
    mark_count = 1
    for i in LED_BIT_RANGE:
        if (mark_count == 0):
            mark_count = 3
            pygame.draw.line(panel, GREY, (led_posnx - 1, LEDAC_POSNY + 10), (led_posnx - 1, LEDAC_POSNY + 15))
        panel.blit(led_off, (led_posnx, LEDAC_POSNY))
        led_posnx += LED_BIT_OFFSETX
        mark_count -= 1

    draw_divider(panel, FILE_ROM_DIVIDER, PANEL_WIDTH)

    panel.blit(font_label.render('pc', 1, BLACK), (LEDPC_POSNX, LEDPC_POSNY + LEDPC_LABEL_OFFSETY))
    led_posnx = LEDPC_POSNX
    mark_count = 1
    for i in LED_BIT_RANGE:
        if (mark_count == 0):
            mark_count = 3
            pygame.draw.line(panel, GREY, (led_posnx - 1, LEDPC_POSNY + 10), (led_posnx - 1, LEDPC_POSNY + 15))
        panel.blit(led_off, (led_posnx, LEDPC_POSNY))
        led_posnx += LED_BIT_OFFSETX
        mark_count -= 1

    draw_divider(panel, ROM_MON_DIVIDERY, PANEL_WIDTH)

    draw_divider(panel, MON_LED_DIVIDERY, PANEL_WIDTH)

    draw_databox(panel, 'l', REGL_BOX_POSNX, REGL_BOX_POSNY, REGL_BOX_WIDTH, REGL_BOX_HEIGHT)
    draw_databox(panel, 'ac', REGAC_BOX_POSNX, REGAC_BOX_POSNY, REGAC_BOX_WIDTH, REGAC_BOX_HEIGHT)
    draw_databox(panel, 'pc', REGPC_BOX_POSNX, REGPC_BOX_POSNY, REGPC_BOX_WIDTH, REGPC_BOX_HEIGHT)

    draw_databox(panel, 'dx', REGDX_BOX_POSNX, REGDX_BOX_POSNY, REGDX_BOX_WIDTH, REGDX_BOX_HEIGHT)
    draw_databox(panel, 'dpc', REGDPC_BOX_POSNX, REGDPC_BOX_POSNY, REGDPC_BOX_WIDTH, REGDPC_BOX_HEIGHT)
    draw_databox(panel, 'dy', REGDY_BOX_POSNX, REGDY_BOX_POSNY, REGDY_BOX_WIDTH, REGDY_BOX_HEIGHT)

    draw_divider(panel, REGS_MON_DIVIDERY, PANEL_WIDTH)

    draw_divider(panel, BOX_BOT_DIVIDERY, PANEL_WIDTH)

    panel.blit(font_label.render('boot rom:', 1, BLACK), BOOTROM_LABEL_POSN)
    draw_checkbox(panel, BOOTROM_WRITABLE_POSN, 0)
    panel.blit(font_label.render('is writable', 1, BLACK), BOOTROM_WRITABLE_LABEL_POSN)
    draw_radiobutton(panel, BOOTROM_LOADPTR_RADIO_POSN, 1)
    panel.blit(font_label.render('papertape', 1, BLACK), BOOTROM_LOADPTR_LABEL_POSN)
    draw_radiobutton(panel, BOOTROM_LOADTTY_RADIO_POSN, 0)
    panel.blit(font_label.render('teletype', 1, BLACK), BOOTROM_LOADTTY_LABEL_POSN)
    
    panel.blit(quit, QUITBUTTON_POSN)
    panel.blit(halt, HALTBUTTON_POSN)
    panel.blit(ss, SINGLESTEPBUTTON_POSN)


def draw_leds(screen, y, value, led_on, led_off):
    posn = LEDAC_SCREEN_POSNX
    for i in LED_BIT_RANGE:
        if (value & 1 << i):
            screen.blit(led_on, (posn, y))
        else:
            screen.blit(led_off, (posn, y))
        posn += LED_BIT_OFFSETX

# Open up a display, draw our loaded image onto it -- check for ESC; if pressed, exit...
#
def main():
    # Setup a 1280x1024 screen...
    screen = pygame.display.set_mode((1280,1024), HWSURFACE|DOUBLEBUF|FULLSCREEN)
    
    # Make a "surface" which is the same size as our screen...
    background = pygame.Surface((1024,1024))

    # Make this background surface a black colour (note: R,G,B tuple):
    background.fill((0,0,0))

    # Load our images
    panel = pygame.image.load(os.path.join('images', 'panel.png'))
    led_off = pygame.image.load(os.path.join('images', 'led_off.png'))
    led_on = pygame.image.load(os.path.join('images', 'led_on.png'))
    quit_button = pygame.image.load(os.path.join('images', 'quit.png'))
    halt_button = pygame.image.load(os.path.join('images', 'halt.png'))
    run_button = pygame.image.load(os.path.join('images', 'run.png'))
    singlestep_button = pygame.image.load(os.path.join('images', 'singlestep.png'))

    # Now define some constants
    # Set the Font ..
    on_label = font_data.render('ON', 1, (0,0,0))
    off_label = font_data.render('OFF', 1, (0,0,0))
    eof_label = font_data.render('EOF', 1, (255,0,0))
    file_name = font_data.render('default_game.ptp', 1, (0,0,0))
    file_name2 = font_data.render('DEFAULT_GAME_abcdefghijklmnopqrstuvwxyz.ptp', 1, (0,0,0))

    panel_init(panel, led_on, led_off, halt_button, quit_button, singlestep_button)
            
    screen.blit(background, (0,0))
    screen.blit(panel, (1024,0))

    running = 1
    offset = 0
    one_step = 0
    full_screen = 1

    rom_is_writable = 0
    load_from_ptr = 1

    menu = Menu(DEVICEMENU, 85)

    clock = pygame.time.Clock()

    # Infinite loop to keep the window open until "QUIT" widget is pressed...
    while 1:
        clock.tick(120)
        pygame.event.pump()
        for event in pygame.event.get():
#            if (event.type == VIDEORESIZE):
#                print 'VIDEORESIZE'
#                screen.blit(background, (0,0))
#                pygame.display.flip()
            if (event.type == MOUSEBUTTONUP):
                if (event.button == 3):
                    if (ptrfilename_rect.collidepoint(event.pos)):
                        menuitem = menu.show(screen, event.pos)
                        if menuitem == 1:
                            pass	# do MOUNT
                        elif menuitem == 2:
                            pass	# do DISMOUNT
                        elif menuitem == 3:
                            pass	# do REWIND
                        elif menuitem == 4:
                            pass	# do MOTOR ON
                        elif menuitem == 5:
                            pass	# do MOTOR OFF
                    if (ptpfilename_rect.collidepoint(event.pos)):
                        menuitem = menu.show(screen, event.pos)
                        if menuitem == 1:
                            pass	# do MOUNT
                        elif menuitem == 2:
                            pass	# do DISMOUNT
                        elif menuitem == 3:
                            pass	# do REWIND
                        elif menuitem == 4:
                            pass	# do MOTOR ON
                        elif menuitem == 5:
                            pass	# do MOTOR OFF
                    if (ttyinfilename_rect.collidepoint(event.pos)):
                        menuitem = menu.show(screen, event.pos)
                        if menuitem == 1:
                            pass	# do MOUNT
                        elif menuitem == 2:
                            pass	# do DISMOUNT
                        elif menuitem == 3:
                            pass	# do REWIND
                        elif menuitem == 4:
                            pass	# do MOTOR ON
                        elif menuitem == 5:
                            pass	# do MOTOR OFF
                    if (ttyoutfilename_rect.collidepoint(event.pos)):
                        menuitem = menu.show(screen, event.pos)
                        if menuitem == 1:
                            pass	# do MOUNT
                        elif menuitem == 2:
                            pass	# do DISMOUNT
                        elif menuitem == 3:
                            pass	# do REWIND
                        elif menuitem == 4:
                            pass	# do MOTOR ON
                        elif menuitem == 5:
                            pass	# do MOTOR OFF

#                     pygame.image.save(screen, snapshot_file)

#                    if (full_screen):
#                        pygame.display.set_mode((100, 100))
#                    else:
#                        pygame.display.set_mode((1280,1024), HWSURFACE|DOUBLEBUF|FULLSCREEN)
#                    full_screen = not full_screen
                if (romwritable_rect.collidepoint(event.pos)):
                    if (rom_is_writable):
                        screen.blit(checkbox_off, SCREEN_BOOTROM_WRITABLE_POSN)
                        panel.blit(checkbox_off, BOOTROM_WRITABLE_POSN)
                        pygame.display.flip()
                        rom_is_writable = 0
                    else:
                        screen.blit(checkbox_on, SCREEN_BOOTROM_WRITABLE_POSN)
                        panel.blit(checkbox_on, BOOTROM_WRITABLE_POSN)
                        pygame.display.flip()
                        rom_is_writable = 1
                if (loadptrradio_rect.collidepoint(event.pos)):
                    if (not load_from_ptr):
                        screen.blit(radiobutton_on, SCREEN_BOOTROM_LOADPTR_RADIO_POSN)
                        panel.blit(radiobutton_on, BOOTROM_LOADPTR_RADIO_POSN)
                        screen.blit(radiobutton_off, SCREEN_BOOTROM_LOADTTY_RADIO_POSN)
                        panel.blit(radiobutton_off, BOOTROM_LOADTTY_RADIO_POSN)
                        pygame.display.flip()
                        load_from_ptr = 1
                if (loadttyradio_rect.collidepoint(event.pos)):
                    if (load_from_ptr):
                        screen.blit(radiobutton_off, SCREEN_BOOTROM_LOADPTR_RADIO_POSN)
                        panel.blit(radiobutton_off, BOOTROM_LOADPTR_RADIO_POSN)
                        screen.blit(radiobutton_on, SCREEN_BOOTROM_LOADTTY_RADIO_POSN)
                        panel.blit(radiobutton_on, BOOTROM_LOADTTY_RADIO_POSN)
                        pygame.display.flip()
                        load_from_ptr = 0
                if (halt_rect.collidepoint(event.pos)):
                    if (running):
                        screen.blit(run_button, SCREEN_HALTBUTTON_POSN)
                        panel.blit(run_button, HALTBUTTON_POSN)
                        pygame.display.flip()
                        running = 0
                    else:
                        screen.blit(halt_button, SCREEN_HALTBUTTON_POSN)
                        panel.blit(halt_button, HALTBUTTON_POSN)
                        pygame.display.flip()
                        running = 1
                if (quit_rect.collidepoint(event.pos)):
                    if (running):
                        screen.blit(run_button, SCREEN_HALTBUTTON_POSN)
                        panel.blit(run_button, HALTBUTTON_POSN)
                        pygame.display.flip()
                        running = 0
                    else:
                        sys.exit()
                if (singlestep_rect.collidepoint(event.pos)):
                    if (running):
                        screen.blit(run_button, SCREEN_HALTBUTTON_POSN)
                        panel.blit(run_button, HALTBUTTON_POSN)
                        pygame.display.flip()
                        running = 0
                    else:
                        one_step = 1

        if running or one_step:
            one_step = 0

            # draw on 'screen'
            offset += 2
            if (offset >= CANVAS_WIDTH):
                offset = 0
            pygame.draw.line(background, YELLOW, (0,offset), (CANVAS_WIDTH - 1,offset))
            pygame.draw.line(background, YELLOW, (offset, 0), (offset, CANVAS_WIDTH - 1))
            pygame.draw.line(background, YELLOW, (0,CANVAS_WIDTH-offset), (CANVAS_WIDTH - 1,CANVAS_WIDTH-offset))
            pygame.draw.line(background, YELLOW, (CANVAS_WIDTH-offset, 0), (CANVAS_WIDTH-offset, CANVAS_WIDTH - 1))
            screen.blit(background, (0,0))

            # draw on the 'control panel'
            screen.blit(panel, (CANVAS_WIDTH,0))
            draw_leds(screen, LEDAC_SCREEN_POSNY, offset, led_on, led_off)
            draw_leds(screen, LEDPC_SCREEN_POSNY, 0xffff - offset, led_on, led_off)
            update_octalbox(screen, CANVAS_WIDTH + REGL_BOX_POSNX, REGL_BOX_POSNY, '%1.1o', 0)
            update_octalbox(screen, CANVAS_WIDTH + REGAC_BOX_POSNX, REGAC_BOX_POSNY, '%6.6o', offset)
            update_octalbox(screen, CANVAS_WIDTH + REGPC_BOX_POSNX, REGPC_BOX_POSNY, '%6.6o', 0xffff - offset)
            screen.blit(off_label, PTR_OFF_POSN)
            screen.blit(eof_label, PTR_EOF_POSN)
            screen.blit(file_name, PTR_FILE_POSN)
            screen.blit(on_label, PTP_ON_POSN)
            screen.blit(eof_label, PTP_EOF_POSN)
            screen.blit(file_name, PTP_FILE_POSN)
            screen.blit(off_label, TTYIN_OFF_POSN)
            screen.blit(file_name, TTYIN_FILE_POSN)
            screen.blit(on_label, TTYOUT_ON_POSN)
            screen.blit(file_name2, TTYOUT_FILE_POSN)

            pygame.display.flip()

            background.fill(BLACK)
    pygame.quit()

# So we can run straight from the CLI...
if __name__ == '__main__':
    main()

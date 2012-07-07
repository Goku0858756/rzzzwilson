#!/usr/bin/env python

import wx 

WIDTH_SCREEN = 1024
HEIGHT_SCREEN = 1024
WIDTH_CONSOLE = 330 # 400 # 256
HEIGHT_CONSOLE = HEIGHT_SCREEN

SCREEN_COLOUR = (0, 0, 0)
CONSOLE_COLOUR = (255, 223, 169)
#PHOSPHOR_COLOUR = '#F0F000'	# yellow
PHOSPHOR_COLOUR = '#40FF40'	# green

V_MARGIN = 20
CTL_MARGIN = 15
LED_MARGIN = 5

IMAGE_LED_OFF = 'images/led_off.png'
IMAGE_LED_ON = 'images/led_on.png'

INC = 0.01

count = 1

class Led_1(object):
    def __init__(self, parent, label, x, y, off, on):
        wx.StaticText(parent, -1, label, pos=(x, y))
        y += 15
        wx.StaticBitmap(parent, -1, off, pos=(x-1, y))
        self.led = wx.StaticBitmap(parent, -1, on, pos=(x-1, y))
        self.set_value(0)

    def set_value(self, value):
        if value:
            self.led.Enable()
        else:
            self.led.Disable()
        

class Led_16(object):
    def __init__(self, parent, label, x, y, off, on):
        led_width = off.GetWidth()
        led_height = off.GetHeight()
        wx.StaticText(parent, -1, label, pos=(x, y))
        y += 15
        self.leds = []
        mark_count = 2
        ticks = [(x-17+led_width,y+led_height/2+5)]
        dc = wx.PaintDC(parent)
        for i in range(16):
            wx.StaticBitmap(parent, -1, off, pos=(x-1+i*17, y))
            led = wx.StaticBitmap(parent, -1, on, pos=(x-1+i*17, y))
            self.leds.append(led)
            mark_count += 1
            if mark_count >= 3:
                mark_count = 0
                ticks.append((x+i*17 + led_width, y+led_height/2+5))

        self.set_value(0)
        self.ticks = ticks

    def set_value(self, value):
        mask = 0x8000
        for l in self.leds:
            if value & mask:
                l.Enable()
            else:
                l.Disable()
            mask = mask >> 1
        

class MyFrame(wx.Frame): 
    """a frame with two panels"""
    def __init__(self, parent=None, id=-1, title=None): 
        wx.Frame.__init__(self, parent, id, title) 
        self.panel_Screen = wx.Panel(self,
                                     size=(WIDTH_SCREEN, HEIGHT_SCREEN),
                                     pos=(0,0)) 
        self.panel_Screen.SetBackgroundColour(SCREEN_COLOUR)
        self.panel_Screen.Bind(wx.EVT_PAINT, self.on_paint) 
        self.panel_Console = wx.Panel(self, style=wx.SIMPLE_BORDER,
                                      size=(WIDTH_CONSOLE, HEIGHT_SCREEN),
                                      pos=(WIDTH_SCREEN,0)) 
        self.panel_Console.SetBackgroundColour(CONSOLE_COLOUR)
        self.panel_Console.Bind(wx.EVT_PAINT, self.on_paint) 

        python_png = wx.Image('images/PythonPowered.png',
                              wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        python_height = python_png.GetHeight()
        python_width = python_png.GetWidth()

        wxpython_png = wx.Image('images/wxPython2.png',
                                wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        wxpython_height = wxpython_png.GetHeight()
        wxpython_width = wxpython_png.GetWidth()

        h_margin = (WIDTH_CONSOLE - wxpython_width - python_width) / 3

        png_height = max(python_height, wxpython_height) + V_MARGIN

        v_margin = (png_height - python_height)/2
        python_ypos = HEIGHT_CONSOLE - png_height + v_margin
        v_margin = (png_height - wxpython_height)/2
        wxpython_ypos = HEIGHT_CONSOLE -  png_height + v_margin

        wx.StaticBitmap(self.panel_Console, -1, python_png,
                        pos=(h_margin, python_ypos))
        wx.StaticBitmap(self.panel_Console, -1, wxpython_png,
                        pos=(python_width + 2*h_margin, wxpython_ypos))

        self.png_height = png_height

        led_off = wx.Image('images/led_off.png',
                           wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        led_on = wx.Image('images/led_on.png',
                          wx.BITMAP_TYPE_PNG).ConvertToBitmap()

        y_pos = 8
        self.led_l = Led_1(self.panel_Console, 'l', CTL_MARGIN, y_pos,
                           led_off, led_on)
        self.led_ac = Led_16(self.panel_Console, 'ac', 3*CTL_MARGIN, y_pos,
                             led_off, led_on)
        y_pos += 35
        self.led_pc = Led_16(self.panel_Console, 'pc', 3*CTL_MARGIN, y_pos,
                             led_off, led_on)


        y_pos = 305
        wx.StaticText(self.panel_Console, -1, 'ptr', pos=(CTL_MARGIN, y_pos))
        y_pos += 15
        self.txt_ptrFile = wx.TextCtrl(self.panel_Console, -1,
                                       pos=(CTL_MARGIN, y_pos),
                                       size=(WIDTH_CONSOLE-2*CTL_MARGIN, 25))
        y_pos += 30

        wx.StaticText(self.panel_Console, -1, 'ptp', pos=(CTL_MARGIN, y_pos))
        y_pos += 15
        self.txt_ptpFile = wx.TextCtrl(self.panel_Console, -1,
                                       pos=(CTL_MARGIN, y_pos),
                                       size=(WIDTH_CONSOLE-2*CTL_MARGIN, 25))
        y_pos += 15

        dc = wx.PaintDC(self.panel_Console)
        dc.SetPen(wx.Pen('black', 1))
        dc.DrawLine(0, HEIGHT_CONSOLE - self.png_height,
                    WIDTH_CONSOLE-1, HEIGHT_CONSOLE - self.png_height)

        for (x, y) in self.led_ac.ticks:
            dc.DrawLine(x, y, x, y+5)
        first = self.led_ac.ticks[0]
        last = self.led_ac.ticks[-1]
        (x1, y1) = first
        (x2, y2) = last
        dc.DrawLine(x1, y2+5, x2, y2+5)

        for (x, y) in self.led_pc.ticks:
            dc.DrawLine(x, y, x, y+5)
        first = self.led_pc.ticks[0]
        last = self.led_pc.ticks[-1]
        (x1, y1) = first
        (x2, y2) = last
        dc.DrawLine(x1, y2+5, x2, y2+5)

        self.y_offset = 0
        self.y_sign = +1

        self.Fit() 

    def on_paint(self, event):
        global count

        # establish the painting surface
        dc = wx.PaintDC(self.panel_Screen)
        dc.SetBackground(wx.Brush(SCREEN_COLOUR, 1))
        dc.SetPen(wx.Pen(PHOSPHOR_COLOUR, 1))
        dc.Clear()
        if self.y_sign > 0:
            self.y_offset = self.y_offset + INC
            if self.y_offset > HEIGHT_SCREEN-1:
                self.y_sign = -1
                self.y_offset = HEIGHT_SCREEN-1
        else:
            self.y_offset = self.y_offset - INC
            if self.y_offset < 0:
                self.y_sign = +1
                self.y_offset = 0
        dc.DrawLine(0, int(self.y_offset), WIDTH_SCREEN-1, int(HEIGHT_SCREEN-self.y_offset-1))
        dc.DrawLine(0, int(HEIGHT_SCREEN-self.y_offset-1), WIDTH_SCREEN-1, int(self.y_offset))

        dc = wx.PaintDC(self.panel_Console)
        #dc.SetPen(wx.Pen('black', wx.DOT))
        dc.SetPen(wx.Pen('black', 1))
        dc.DrawLine(0, HEIGHT_CONSOLE - self.png_height,
                    WIDTH_CONSOLE-1, HEIGHT_CONSOLE - self.png_height)

        for (x, y) in self.led_ac.ticks:
            dc.DrawLine(x, y, x, y+5)
        first = self.led_ac.ticks[0]
        last = self.led_ac.ticks[-1]
        (x1, y1) = first
        (x2, y2) = last
        dc.DrawLine(x1, y2+5, x2, y2+5)

        for (x, y) in self.led_pc.ticks:
            dc.DrawLine(x, y, x, y+5)
        first = self.led_pc.ticks[0]
        last = self.led_pc.ticks[-1]
        (x1, y1) = first
        (x2, y2) = last
        dc.DrawLine(x1, y2+5, x2, y2+5)

        count += 1
        self.led_ac.set_value(count)


# test it ...
app = wx.PySimpleApp() 
frame1 = MyFrame(title='pymlac 0.1') 
frame1.Center() 
frame1.Show() 
app.MainLoop()
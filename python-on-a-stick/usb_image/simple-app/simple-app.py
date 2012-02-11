# -*- coding: utf-8 -*-

"""
A simple wxPython application designed to run from a USB memory stick.

The code here shamelessly copied from
    [http://wiki.wxpython.org/wxPython%20by%20Example]
"""

import sys
import time
import wx
import wx.html


# path to  file with 'About' text
# note the 'driveless' path so we work no matter what drive USB stick mounts as
AboutFile = '/about.txt'


class HtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, id, size=(600,400)):
        wx.html.HtmlWindow.__init__(self, parent, id, size=size)

    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())
        
class AboutBox(wx.Dialog):
    def __init__(self):
        # get the time we read the HTML file
        read_time = time.asctime()

        # get file contents
        with open(AboutFile, 'rb') as fd:
            lines = fd.readlines()

        # update the file contents with last-read time
        for (i, line) in enumerate(lines):
            if line.startswith('Last updated'):
                lines[i] = 'Last updated on %s\n' % time.asctime()
                break

        with open(AboutFile, 'wb') as fd:
            for line in lines:
                fd.write(line)
                
        about_text = ''.join(lines)

        # display the updated text in an HTML window        
        wx.Dialog.__init__(self, None, wx.ID_ANY, "About simple-app",
                           style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|
                                 wx.RESIZE_BORDER|wx.TAB_TRAVERSAL)
        hwin = HtmlWindow(self, wx.ID_ANY, size=(400,200))
        hwin.SetPage(about_text)
        btn = hwin.FindWindowById(wx.ID_OK)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth()+25, irep.GetHeight()+10))
        self.SetClientSize(hwin.GetSize())
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()

class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, pos=(150,150),
                          size=(350,200))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        m_close = wx.Button(panel, wx.ID_CLOSE, "About")
        m_close.Bind(wx.EVT_BUTTON, self.OnAbout)
        box.Add(m_close, 0, wx.ALL, 10)
        
        panel.SetSizer(box)
        panel.Layout()

    def OnClose(self, event):
        self.Destroy()

    def OnAbout(self, event):
        dlg = AboutBox()
        dlg.ShowModal()
        dlg.Destroy()  


app = wx.App(redirect=True)   # Error messages go to popup window
top = Frame("simple-app")
top.Show()
app.MainLoop()

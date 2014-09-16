import wx
import time

class DrawPanel(wx.ScrolledWindow):
        def __init__(self, parent):
                wx.ScrolledWindow.__init__(self, parent, -1)
                wx.EVT_PAINT(self, self.OnPaint)
                self.SetVirtualSize((512, 512))
                self.SetScrollRate(4, 4)
                self.buffer = wx.EmptyBitmap(512, 512)
                self.firstDraw()

                self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
                self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
                self.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)

                self.dragFlg = False


        def OnMouseLeftDown(self, event):
                dc = wx.BufferedDC(None, self.buffer)
                #dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
                self.SetBackgroundColour("white")
                dc.Clear()

                pos = event.GetPosition()
                self.px = pos[0]
                self.py = pos[1]
                self.dragFlg = True

                self.startTime = int(time.time()*1000)
                self.outputLog("%d\t%d\t%d" % (0, self.px, self.py))


        def OnMouseMotion(self, event):
                if self.dragFlg == True:
                        pos = event.GetPosition()
                        nx = pos[0]
                        ny = pos[1]
                        self.outputLog("%d\t%d\t%d" % (int(time.time()*1000) - self.startTime, nx, ny))


                        dc = wx.BufferedDC(None, self.buffer)
                        dc.SetPen(wx.Pen("BLACK", 2))
                        dc.DrawLine(self.px, self.py, nx, ny)

                        self.px = nx
                        self.py = ny

                        self.Refresh()

        def OnMouseLeftUp(self, event):
                self.dragFlg = False
                self.outputLog()

        def outputLog(self, str = ""):
                print str

        def firstDraw(self):
                dc = wx.BufferedDC(None, self.buffer)
                dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
                dc.Clear()
                #dc.SetPen(wx.Pen("BLACK", 1))
                #dc.DrawCircle(100, 100, 10)
                #dc.DrawCircle(2000, 100, 10)

        def OnPaint(self, event=None):
                dc = wx.BufferedPaintDC(self, self.buffer,
                        wx.BUFFER_VIRTUAL_AREA)

class TopFrame(wx.Frame):
        def __init__(self, parent, ID, name):
                wx.Frame.__init__(self, parent, ID, name)

class MyApp(wx.App):
        def OnInit(self):
                f = TopFrame(None, -1, "Test 1")
                DrawPanel(f)
                f.Show(True)
                self.SetTopWindow(f)
                self.f = f;
                return True

if __name__ == '__main__':
        app = MyApp()
        app.MainLoop()

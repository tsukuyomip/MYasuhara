import wx
import time
import cPickle as cpkl

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
                self.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseRightDown)

                self.dragFlg = False
                self.logData = None

        def OnMouseLeftDown(self, event):
                # initialize canvas
                dc = wx.BufferedDC(None, self.buffer)
                #dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
                #self.SetBackgroundColour("white")
                dc.SetPen(wx.Pen("WHITE", 2))
                dc.DrawRectangle(0, 0, 512, 512)
                dc.Clear()

                # get position & time
                pos = event.GetPosition()
                self.px = pos[0]
                self.py = pos[1]
                self.dragFlg = True
                self.startTime = int(time.time()*1000)

                # initialize log
                self.logData = []
                self.logData.append((0, self.px, self.py))
                self.outputLog("%d\t%d\t%d" % (0, self.px, self.py))


        def OnMouseMotion(self, event):
                if self.dragFlg == True:
                        # get position & time
                        pos = event.GetPosition()
                        nx = pos[0]
                        ny = pos[1]
                        t = int(time.time()*1000) - self.startTime
                        t = int((t/10) + 1)

                        # add log
                        self.logData.append((t, nx, ny))
                        self.outputLog("%d\t%d\t%d" % (t, nx, ny))

                        # draw line
                        dc = wx.BufferedDC(None, self.buffer)
                        dc.SetPen(wx.Pen("BLACK", 2))
                        dc.DrawLine(self.px, self.py, nx, ny)

                        # update previous x, y
                        self.px = nx
                        self.py = ny

                        # show
                        self.Refresh()

        def OnMouseLeftUp(self, event):
                self.dragFlg = False
                self.outputLog()

        def OnMouseRightDown(self, event):
                # if drawn, dump logData
                if self.logData != None:
                        filename = "testLog.pkl"
                        cpkl.dump(self.logData, open(filename, "wb"))
                        print "output logfile:", filename

        def outputLog(self, str = ""):
                print str

        def firstDraw(self):
                dc = wx.BufferedDC(None, self.buffer)
                dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
                dc.Clear()
                dc.SetPen(wx.Pen("#FF9999", 2))
                dc.DrawRectangle(0, 0, 512, 512)
                #dc.SetPen(wx.Pen("BLACK", 1))
                #dc.DrawCircle(100, 100, 10)
                #dc.DrawCircle(2000, 100, 10)

        def OnPaint(self, event=None):
                dc = wx.BufferedPaintDC(self, self.buffer,
                        wx.BUFFER_VIRTUAL_AREA)

class TopFrame(wx.Frame):
        def __init__(self, parent, ID, name):
                wx.Frame.__init__(self, parent, ID, name, size=(550,550))

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

# encoding: utf-8
import wx

class MainFrame(wx.Frame):
    def __init__(self,parent=None):
        pre=wx.PreFrame()
        XRC().LoadOnFrame(pre,parent,'MainFrame')
        self.PostCreate(pre)

def main():
    app = wx.App()                               # アプリケーションのインスタンス作成
    wx_utils.XrcInit("resource/resource.xrc")    # リソースの初期化
    frame = MainFrame()                          # メインフレーム作成
    app.SetTopWindow(frame)                      # アプリケーションのウィンドウ階層のトップに据える
    frame.Show(True)                             # メインフレームを表示
    app.MainLoop()                               # メインフレーム終了待ち

if __name__=="__main__":
    main()

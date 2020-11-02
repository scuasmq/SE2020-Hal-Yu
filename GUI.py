import wx
from main import *
class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='黄金点数游戏',size = (450,300))
        #### 游戏数据
        self.player_num = 0
        self.golen_score = 0

        #### 组件
        panel = wx.Panel(self)
        self.txt = TransparentStaticText(panel,-1,label = 'hello world',pos=(10,10))
        self.txt.Hide()
        # self.txt1 = wx.StaticText(panel, -1, label='hello world', pos=(10, 10))
        self.strt_btn = wx.Button(panel, label='开始游戏', pos=(200, 125))
        self.ctnu_btn = wx.Button(panel,label = '继续游戏',pos = (30,220))
        self.ctnu_btn.Hide()
        self.show_btn = wx.Button(panel,label = '显示分数',pos = (180,220))
        self.show_btn.Hide()
        self.exit_btn = wx.Button(panel,label = '结束游戏',pos = (320,220))
        self.exit_btn.Hide()

        self.player_numText = wx.StaticText(panel,-1,label='请输入玩家人数',pos=(10,70),size=(-1,-1))
        self.player_numTxcl = wx.TextCtrl(panel,-1,value='',pos=(120,70),size = (100,20))
        #### 绑定事件
        self.strt_btn.Bind(wx.EVT_BUTTON,self.onClickStrtButton)
        self.exit_btn.Bind(wx.EVT_BUTTON,self.onClickExitButton)
        self.player_numTxcl.Bind(wx.EVT_TEXT,self.getInputPlayerNum)

        self.Show()

    def onClickStrtButton(self,event):
        self.strt_btn.Hide()
        self.ctnu_btn.Show()
        self.show_btn.Show()
        self.exit_btn.Show()
        print("hello world")
        pass
    def onClickExitButton(self,event):
        print('exit')
        self.Destroy()
    def getInputPlayerNum(self,event):
        self.player_num = int(self.player_numTxcl.GetValue())
        print(self.player_num)
        pass
####这个类是用来实现透明控件的
class TransparentStaticText(wx.StaticText):
    def __init__(self, parent, id=wx.ID_ANY, label='', pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.TRANSPARENT_WINDOW, name='TransparentStaticText'):
        wx.StaticText.__init__(self, parent, id, label, pos, size, style, name)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnPaint(self, event):
        bdc = wx.PaintDC(self)
        dc = wx.GCDC(bdc)
        font_face = self.GetFont()
        font_color = self.GetForegroundColour()
        dc.SetFont(font_face)
        dc.SetTextForeground(font_color)
        dc.DrawText(self.GetLabel(), 0, 0)

    def OnSize(self, event):
        self.Refresh()
        event.Skip()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()

import wx
class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Test",size = (300,300))
        self.panel = wx.Panel(self)
        self.text = wx.TextCtrl(self.panel,-1,value='',pos=(10,10),size=(100,30))
        self.button = wx.Button(self.panel,-1,label='button',pos=(60,60),size=(60,60))
        self.button.Enable(False)
        self.Bind(wx.EVT_TEXT,self.OnEnter,self.text)
        self.resultText = wx.StaticText(self.panel, -1,label='123',pos=(10,70),size=(-1,-1))
    def OnEnter(self,evt):
        try:
            z = False
            z = type(eval(self.text.GetValue())) == int or type(eval(self.text.GetValue())) == float
        except:
            pass
        if z:
            self.resultText.SetLabel('T')
            # self.resultText.Hide()
            # self.resultText.Sho
            self.button.Enable(True)
        else:
            self.resultText.SetLabel('F')
            self.button.Enable(False)
app = wx.PySimpleApp()
TestFrame().Show()
app.MainLoop()
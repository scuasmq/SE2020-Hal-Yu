import wx
class MyFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title='',
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE,
                 name='MyFrame'):
        super(MyFrame, self).__init__(parent, id, title, pos,
                                      size, style, name)
        self.panel = wx.Panel(self)
        self.txtCtrl = wx.TextCtrl(self.panel,
                                   style=wx.TE_MULTILINE)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.txtCtrl, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)
        self.CreateStatusBar()

        self.txtCtrl.Bind(wx.EVT_KEY_DOWN , self.onKeyDown)  # 键盘监听事件，只能绑定在那种，支持键盘的控件中（即 keyborad focus）
        self.txtCtrl.Bind(wx.EVT_CHAR, self.onChar)
        self.txtCtrl.Bind(wx.EVT_KEY_UP, self.onKeyUp)

    def onKeyDown(self, event):
        print('onKeyDown called')
        key_code = event.GetKeyCode()
        raw_code = event.GetRawKeyCode()  # key_code 和 raw_code 似乎没什么区别，打印出来都是一样的。应该差别是在编码方式的不同吧。
        modifiers = event.GetModifiers()
        # 所谓 modifiers 就是键盘上的 Ctrl 键之类的。
        msg = "key:%d,raw:%d,modifier:%d" % (key_code,
                                             raw_code, modifiers)
        self.PushStatusText("KeyDown: " + msg)
        event.Skip()  # 如果不加上这句代码，那么 onChar、onKeyup 就不会被运行。

    def onChar(self, event):
        print('onChar called')
        key_code = event.GetKeyCode()
        raw_code = event.GetRawKeyCode()
        modifiers = event.GetModifiers()
        msg = 'key:%d,raw:%d,modifier:%d' % (key_code,
                                             raw_code, modifiers)

        if modifiers & wx.MOD_SHIFT:
            wx.Bell()  # 响一下而已，别怕。
        elif chr(key_code) in 'aeiou':
            self.txtCtrl.AppendText('?')
        else:
            event.Skip()

    def onKeyUp(self, event):
        print('onKeyUp called')
        event.Skip()


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title='My App')
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


app = MyApp(False)
app.MainLoop()
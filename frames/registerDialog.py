import wx


class RegisterDialog(wx.Dialog):
    def __init__(self, title, func_callBack, themeColor):
        wx.Dialog.__init__(self, None, -1, title, size=(300, 200))
        self.func_callBack = func_callBack
        self.themeColor = themeColor

        self.InitUI()  # 绘制Dialog的界面

    def InitUI(self):
        panel = wx.Panel(self)

        font = wx.Font(14, wx.DEFAULT, wx.BOLD, wx.NORMAL, True)

        accountLabel = wx.StaticText(panel, -1, '账号', pos=(20, 25))
        accountLabel.SetFont(font)

        self.accountInput = wx.TextCtrl(panel, -1, u'', pos=(80, 25), size=(180, -1))
        self.accountInput.SetForegroundColour('gray')
        self.accountInput.SetFont(font)

        passwordLabel1 = wx.StaticText(panel, -1, '密码', pos=(20, 70))
        passwordLabel1.SetFont(font)
        self.passwordInput1 = wx.TextCtrl(panel, -1, u'', pos=(80, 70), size=(180, -1), style=wx.TE_PASSWORD)
        self.passwordInput1.SetFont(font)

        passwordLabel2 = wx.StaticText(panel, -1, '再次输入', pos=(20, 100))
        passwordLabel2.SetFont(font)
        self.passwordInput2 = wx.TextCtrl(panel, -1, u'', pos=(80, 100), size=(180, -1), style=wx.TE_PASSWORD)
        self.passwordInput2.SetFont(font)

        sureButton = wx.Button(panel, -1, u'注册', pos=(20, 130), size=(120, 40))
        self.Bind(wx.EVT_BUTTON, self.sureEvent, sureButton)

        cancleButton = wx.Button(panel, -1, u'取消', pos=(160, 130), size=(120, 40))

        # 为【取消Button】绑定事件
        self.Bind(wx.EVT_BUTTON, self.cancleEvent, cancleButton)

    def sureEvent(self, event):
        account = self.accountInput.GetValue()
        password1 = self.passwordInput1.GetValue()
        password2 = self.passwordInput2.GetValue()
        if password1!=password2:
            wx.MessageBox('两次输入的密码不一致','注册失败')
            return
        # 通过回调函数传递数值
        self.func_callBack(account, password1)
        self.Destroy()  # 销毁隐藏Dialog

    def cancleEvent(self, event):
        self.Destroy()  # 销毁隐藏Dialog
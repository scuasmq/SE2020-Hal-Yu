import wx
from Utils import sendUtils
from frames import registerDialog


class LoginFrame(wx.Frame):
    def __init__(self,sock,parent=None,id=-1,updateFrame = None):
        super(LoginFrame, self).__init__(parent=None,title = '黄金点数游戏',size = (400,350))
        self.panel = wx.Panel(self,-1)
        self.sock = sock
        self.updateFrame = updateFrame

        # v_box_sizer = wx.BoxSizer(wx.VERTICAL)

        self.bt_confirm = wx.Button(self.panel, label="登陆")  # 创建按钮
        self.bt_confirm.Bind(wx.EVT_BUTTON, self.OnclickSubmit)
        self.bt_cancel = wx.Button(self.panel, label="注册")
        self.bt_cancel.Bind(wx.EVT_BUTTON, self.OnclickRegister)

        self.title = wx.StaticText(self.panel, label="登陆")

        self.label_user = wx.StaticText(self.panel, label="用户名:")
        self.text_user = wx.TextCtrl(self.panel, style=wx.TE_LEFT)

        self.label_pwd = wx.StaticText(self.panel, label="密   码:")
        self.text_password = wx.TextCtrl(self.panel, style=wx.TE_PASSWORD)
        # 控件横向排列
        hsizer_user = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_user.Add(self.label_user, proportion=0, flag=wx.ALL, border=5)
        hsizer_user.Add(self.text_user, proportion=1, flag=wx.ALL, border=5)  # proportion=0表示不变,proportion=1两倍宽度

        hsizer_pwd = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_pwd.Add(self.label_pwd, proportion=0, flag=wx.ALL, border=5)
        hsizer_pwd.Add(self.text_password, proportion=1, flag=wx.ALL, border=5)

        hsizer_button = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_button.Add(self.bt_confirm, proportion=0, flag=wx.ALIGN_CENTER, border=5)
        hsizer_button.Add(self.bt_cancel, proportion=1, flag=wx.ALIGN_CENTER, border=5)
        # 控件纵向排列
        vsizer_all = wx.BoxSizer(wx.VERTICAL)
        vsizer_all.Add(self.title, proportion=0, flag=wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER, border=15)

        vsizer_all.Add(hsizer_user, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=45)
        vsizer_all.Add(hsizer_pwd, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=45)
        vsizer_all.Add(hsizer_button, proportion=0, flag=wx.ALIGN_CENTER, border=15)
        self.panel.SetSizer(vsizer_all)

        font = wx.Font(16, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL, underline=False)
        self.title.SetFont(font)


    def validUser(self,soc):
        data = soc.recv(1024)
        jsdata = eval(data)
        print('jsdata'+str(jsdata))
        if(jsdata['MESSAGE']=='success'):
            return True
        else:
            return False
    def valiRegister(self,soc):
        data = soc.recv(1024)
        jsdata = eval(data)
        if(jsdata['MESSAGE']=='success'):
            return True
        else:
            return False

    def OnclickSubmit(self, event):
        self.username = self.text_user.GetValue()
        self.password = self.text_password.GetValue()
        sendUtils.c_sendLogInfo(self.sock, self.username, self.password)

        if(self.validUser(self.sock)):
            # self.panel.Parent.Hide()
            # app = roomFrame.MainApp()
            # app.MainLoop()
            self.updateFrame(1)
        else:
            message = '登陆失败，用户名或密码错误'
            wx.MessageBox(message,'登陆失败')

    def OnclickRegister(self, event): #注册
        dlg = RegisterWindow(self.getRegisterInfo,'#0a74f7')
        dlg.Show()

    def getRegisterInfo(self,username,password):
        self.r_username = username
        self.r_password = password
        sendUtils.c_sendRegisterInfo(self.sock, self.r_username, self.r_password)
        print('callback'+username)
        if(self.valiRegister(self.sock)):
            return
        else:
            wx.MessageBox('注册失败','失败信息')


class RegisterWindow(registerDialog.RegisterDialog):
    def __init__(self,callback_func,themeColor):
        registerDialog.RegisterDialog.__init__(self, '注册', callback_func, themeColor)

import wx
from Utils import sendUtils


class RoomFrame(wx.Frame):
    def __init__(self, sock,parent=None,id=-1,updateFrame = None):
        wx.Frame.__init__(self, parent, -1, title="游戏房间", size=(400, 250),
                          style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.panel = wx.Panel(self,-1)
        self.sock = sock
        self.updateFrame = updateFrame
        self.username = self.getUsername(self.sock)
        self.gameid = 0


        print('self.username:',self.username)
        self.initUI()

    def initUI(self):
        self.bt_create = wx.Button(self.panel,label="创建房间")
        self.bt_create.Bind(wx.EVT_BUTTON, self.OnclickCreate)
        self.bt_enter = wx.Button(self.panel,label="加入房间")
        self.bt_enter.Bind(wx.EVT_BUTTON,self.OnclickEnter)
        hsizer_control = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_control.Add(self.bt_create,proportion=0,flag=wx.ALL,border=5)
        hsizer_control.Add(self.bt_enter,proportion=0,flag=wx.ALL,border=5)

        self.label_name = wx.StaticText(self.panel,label="房间名")
        self.text_name = wx.TextCtrl(self.panel,style=wx.TE_LEFT)
        self.label_num = wx.StaticText(self.panel,label="房间人数")
        self.text_num = wx.TextCtrl(self.panel,style=wx.TE_LEFT)
        self.label_epoch = wx.StaticText(self.panel,label="轮数")
        self.text_epoch = wx.TextCtrl(self.panel, style=wx.TE_LEFT)

        hsizer_input1 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_input1.Add(self.label_name,proportion=0,flag=wx.ALL,border=5)
        hsizer_input1.Add(self.text_name, proportion=1, flag=wx.ALL, border=5)

        hsizer_input2 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_input2.Add(self.label_num, proportion=0, flag=wx.ALL, border=5)
        hsizer_input2.Add(self.text_num, proportion=1, flag=wx.ALL, border=5)
        hsizer_input2.Add(self.label_epoch, proportion=0, flag=wx.ALL, border=5)
        hsizer_input2.Add(self.text_epoch, proportion=1, flag=wx.ALL, border=5)

        self.title = wx.StaticText(self.panel, label="游戏大厅")
        font = wx.Font(16, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL, underline=False)
        self.title.SetFont(font)
        vsizer_all = wx.BoxSizer(wx.VERTICAL)
        vsizer_all.Add(self.title, proportion=0, flag=wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER, border=15)
        vsizer_all.Add(hsizer_input1, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=45)
        vsizer_all.Add(hsizer_input2, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=45)
        vsizer_all.Add(hsizer_control, proportion=0, flag=wx.ALIGN_CENTER, border=15)
        self.panel.SetSizer(vsizer_all)

    def OnclickCreate(self,event):
        roomname = self.text_name.GetValue()
        maxnum = self.text_num.GetValue()
        epochnum = self.text_epoch.GetValue()
        sendUtils.c_createRoom(self.sock,roomname,maxnum,self.username,epochnum)
        if self.validCreate(self.sock):
            self.updateFrame(2,roomname,self.gameid,self.username)  #playerid == 0
        else:
            wx.MessageBox('创建房间失败，请更换房间名','创建失败')
    def OnclickEnter(self,event):
        roomname = self.text_name.GetValue()
        sendUtils.c_enterRoom(self.sock,roomname,self.username)
        if self.validEnter(self.sock):
            self.updateFrame(2,roomname,self.gameid,self.username)
        else:
            wx.MessageBox('加入房间失败（房间不存在或人数已满）','加入失败')

    def validCreate(self,soc):
        data = soc.recv(1024)
        jsdata = eval(data)
        if(jsdata['MESSAGE']=='success'):
            self.gameid = jsdata['gameid']
            return True
        else:
            return False

    def validEnter(self,soc):
        data = soc.recv(1024)
        jsdata = eval(data)
        if(jsdata['MESSAGE']=='success'):
            self.gameid = jsdata['gameid']
            self.playerid = jsdata['playerid']
            return True
        else:
            return False

    def getUsername(self,soc):
        sendUtils.c_getUsername(soc)
        data = soc.recv(1024)
        jsdata = eval(data)
        return jsdata['MESSAGE']

class MainApp(wx.App):
    def OnInit(self):
        self.frame = RoomFrame(None)
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = MainApp()
    app.MainLoop()

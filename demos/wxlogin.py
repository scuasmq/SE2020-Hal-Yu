import wx
import time
import sqlite3
from frames import roomFrame


class MyFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, title="创建Frame", size=(400, 300),
                          name='frame')  # 如果是顶级窗口，这个值是None,id=-1自动生成 ,name框架内的文字
        self.panel = wx.Panel(self)
        # icon = wx.Icon('smart.ico')
        # self.SetIcon(icon)
        self.bt_confirm = wx.Button(self.panel, label="确定")  # 创建按钮
        self.bt_confirm.Bind(wx.EVT_BUTTON, self.OnclickSubmit)
        self.bt_cancel = wx.Button(self.panel, label="取消")
        self.bt_cancel.Bind(wx.EVT_BUTTON, self.OnclickCancel)

        self.title = wx.StaticText(self.panel, label="请输入用户名和密码")  # ,style=0  #相当于tkinter中的Label

        self.label_user = wx.StaticText(self.panel, label="用户名:")
        self.text_user = wx.TextCtrl(self.panel, style=wx.TE_LEFT)  # 相当于tkinter的Entry

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

    def OnclickSubmit(self, event):
        username = self.text_user.GetValue()
        password = self.text_password.GetValue()
        self.conn = sqlite3.connect('../database.db')
        curs = self.conn.cursor()
        query = "select Username,Password,error,isActive from user_info where Username='%s'" % username
        curs.execute(query)  # 返回一个迭代器
        c = curs.fetchall()  # 接收全部信息

        if len(c) == 0:
            # self.root.withdraw()
            message = '登录失败账户不存在'
            wx.MessageBox(message)
        else:
            us, pw, error, isActive = c[0]
            if isActive == "N":
                message = '登录失败用户还未激活!'
                wx.MessageBox(message)
            else:
                if error >= 3:
                    message = '登录失败错误超过三次账户已被锁定'
                    wx.MessageBox(message)
                elif us == username and pw == password:
                    # self.panel.Show(False)

                    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    sql = "UPDATE user_info SET Logindate=" + "'" + date + "'" + " WHERE Username=" + us
                    curs.execute(sql)
                    self.conn.commit()
                    self.conn.close()
                    self.panel.Parent.Hide()
                    app = roomFrame.MainApp()
                    app.MainLoop()
                else:

                    num = int(error) + 1
                    message = '登录失败密码错误' + str(num) + "次"
                    wx.MessageBox(message)

                    self.add_error(us, num)

    def add_error(self, user, num):
        self.conn = sqlite3.connect("../database.db")
        c = self.conn.cursor()
        sql = "UPDATE user_info SET error=" + str(num) + " Where Username =" + user
        # print(sql)
        c.execute(sql)
        li = c.fetchone()
        self.conn.commit()
        self.conn.close()
        return li

    def OnclickCancel(self, event):
        self.text_user.SetValue("")
        self.text_password.SetValue("")


if __name__ == "__main__":
    app = wx.App()  # 创建App类的实例
    frame = MyFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()  # 调用MainLoop()主循环方法


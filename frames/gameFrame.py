import wx
import math
import pymysql
import threading
from Utils import sendUtils
import time
from threading import Timer
class GameFrame(wx.Frame):
    def __init__(self,sock,roomname=None,gameid=None,playername=None,parent=None,id=-1,updateFrame=None):
        wx.Frame.__init__(self,parent=None, title='黄金点数游戏,'+roomname,size = (450,350),style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        self.sock = sock
        self.updateFrame = updateFrame
        self.gameid = gameid
        self.playername = playername
        print('game creator:',self.playername)
        self.roomname = roomname
        print('playerid:',playername)
        waiting_thread = threading.Thread(target=self.waiting,args=(self.sock,))
        waiting_thread.start()

        self.initWidgets()
        self.bindEvents()

        self.Show()

    def initWidgets(self):
        self.panel = wx.Panel(self)
        self.label_waiting = wx.StaticText(self.panel,-1,label = '请等待其他玩家加入',pos=(10,70))
        self.label_waitothers = wx.StaticText(self.panel, -1, label='请等待其他玩家输入', pos=(10, 70))
        self.label_waitothers.Hide()

        self.label_input = wx.StaticText(self.panel,-1,label = '请输入您的点数',pos=(10,70))
        self.text_input = wx.TextCtrl(self.panel,-1,value='',pos=(120,70))
        self.bt_input = wx.Button(self.panel,label='确定',pos = (240,70),size=(60,20))
        self.hideInput()

        self.text_result = wx.StaticText(self.panel,-1,label='',pos=(10,120))
        self.text_wait = wx.StaticText(self.panel,-1,label='五秒后回到输入')
        self.hideResult()

        self.bt_return = wx.Button(self.panel,label='回到房间',pos = (240,70),size=(100,20))
        self.bt_return.Bind(wx.EVT_BUTTON,self.OnclickReturn)
        self.bt_return.Hide()

    def OnclickInput(self,event):
        point = self.text_input.GetValue()
        sendUtils.c_point(self.sock,point,self.playername,self.roomname)
        self.hideInput()
        self.label_waitothers.Show()
        result_thread = threading.Thread(target=self.getResult,args=(self.sock,))
        result_thread.start()

    def OnclickReturn(self,event):
        self.updateFrame(1)
    def bindEvents(self):
        self.bt_input.Bind(wx.EVT_BUTTON,self.OnclickInput)

    def showResult(self):
        self.text_result.Show()
        self.text_wait.Show()
    def hideResult(self):
        self.text_result.Hide()
        self.text_wait.Hide()

    def showInput(self):
        self.label_input.Show()
        self.text_input.Show()
        self.bt_input.Show()

    def hideInput(self):
        self.label_input.Hide()
        self.text_input.Hide()
        self.bt_input.Hide()

    def initData(self):
        self.player_num = 0
        self.golden_score = 0
        self.player_group = []
        self.player_input = []
        self.tmpId = 0
        self.maxId = -1
        self.minId = -1
        # self.player_group.append(Player(str(0)))
        self.conn = pymysql.connect(
            host = "localhost",
            user = "dataUser",
            password = "scusmq61347",
            database = "SE2020",
            charset = "utf8"
        )
        sql_count = 'select count(*) from goldennum'
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql_count)
        self.game_id = self.cursor.fetchone()[0]+1
        self.firstGame = True

    def waiting(self,soc):
        while True:
            time.sleep(0.05)
            sendUtils.c_readyQuery(soc,self.roomname)
            data = soc.recv(1024)
            jsdata = eval(data)
            if(jsdata['MESSAGE']=='OK'):
                self.ready = True
                print('ready ok')
                self.label_waiting.Hide()
                self.showInput()
                return

    def showInputAgain(self):
        self.showInput()
        self.hideResult()

    def getResult(self,soc):
        while True:
            time.sleep(0.05)
            sendUtils.c_resultQuery(soc,self.playername,self.roomname)
            data = soc.recv(1024)
            jsdata = eval(data)
            if(jsdata['MESSAGE']=='OK'):
                self.label_waitothers.Hide()
                self.showResult()
                self.text_result.SetLabel(jsdata['result'])
                end = jsdata['end']
                if not end:
                    t = Timer(5.0,self.showInputAgain)
                    t.start()
                else:
                    self.bt_return.Show()
                    self.text_wait.SetLabel('游戏结束')
                return

if __name__ == '__main__':
    app = wx.App()
    frame = GameFrame(None)
    app.MainLoop()

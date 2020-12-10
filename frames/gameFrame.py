import wx
import math
import pymysql
import threading
from Utils import sendUtils
import time
from threading import Timer
import matplotlib
from matplotlib import pyplot as plt
import wx.grid
import os

matplotlib.use('WXAgg')

class GameFrame(wx.Frame):
    def __init__(self,sock,roomname=None,gameid=None,playername=None,parent=None,id=-1,updateFrame=None):
        wx.Frame.__init__(self,parent=None, title='黄金点数游戏,'+roomname,size = (750,500),style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.sock = sock
        self.updateFrame = updateFrame
        self.gameid = gameid
        self.playername = playername
        print('game creator:',self.playername)
        self.roomname = roomname
        print('playerid:',playername)
        waiting_thread = threading.Thread(target=self.waiting,args=(self.sock,))
        waiting_thread.start()
        self.all_score = {}
        self.all_input = {}

        self.initWidgets()
        self.bindEvents()

        self.Show()

############
    def disableButtons(self):
        self.resultPanelButton.Disable()
        self.graphPanelButton.Disable()

    def initStartPanel(self):
        self.label_waiting = wx.StaticText(
            self.startPanel, -1, label='请等待其他玩家加入', pos=(10, 70))
        self.label_waitothers = wx.StaticText(
            self.startPanel, -1, label='请等待其他玩家输入', pos=(10, 70))
        self.label_waitothers.Hide()

        self.label_input = wx.StaticText(
            self.startPanel, -1, label='请输入您的点数', pos=(10, 70))
        self.text_input = wx.TextCtrl(
            self.startPanel, -1, value='', pos=(120, 70))
        self.bt_input = wx.Button(
            self.startPanel, label='确定', pos=(240, 70), size=(60, 20))
        self.hideInput()

        self.text_result = wx.StaticText(
            self.startPanel, -1, label='', pos=(10, 120))
        self.text_wait = wx.StaticText(self.startPanel, -1, label='五秒后回到输入')
        self.hideResult()

        self.bt_return = wx.Button(
            self.startPanel, label='回到房间', pos=(240, 70), size=(100, 20))
        self.bt_return.Bind(wx.EVT_BUTTON, self.OnclickReturn)
        self.bt_return.Hide()

    def initResultPanel(self):
        self.resultPanelButton.Enable()

        length = len(self.all_input)

        self.resultGrid = wx.grid.Grid(self.resultPanel, -1, size=(500, 400), pos=(20, 20))
        self.resultGrid.CreateGrid(length, 3)
        self.resultGrid.SetColLabelValue(0, "用户名")
        self.resultGrid.SetColLabelValue(1, "输入")
        self.resultGrid.SetColLabelValue(2, "得分")
        for i,(name,input) in enumerate(self.all_input.items()):
            self.resultGrid.SetCellValue(i, 0, name)
            self.resultGrid.SetCellValue(i, 1, str(input))
            self.resultGrid.SetCellValue(i, 2, str(self.all_score[name]))

    def initGraphPanel(self):
        self.graphPanelButton.Enable()
        print('玩家输入:',self.all_input)
        inputs = list(self.all_input.values())
        # inputs = [10, 12, 13,15,16,20,25,34,46,56,76,43,7,76,8,76,54,63,72,83,41]
        group = range(0, 101, 1)
        plt.hist(inputs, group, rwidth=0.8)  # density=False would make counts
        plt.grid(alpha=0.3)
        plt.savefig('hist.jpg')

        self.img = wx.Image('hist.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.bitmapGraph = wx.StaticBitmap(self.graphPanel, -1, self.img, (0, 0))

        self.bitmapGraph.Show()
############

    def setRoomName(self,roomname):
        self.roomname = roomname
        self.SetTitle('黄金点数游戏,'+self.roomname)
    def initWidgets(self):
        self.panel = wx.Panel(self)
        self.sidebar = wx.Panel(self.panel, size=(64, 600))
        self.mainPanel = wx.Panel(self.panel, size=(700, 600))
        self.mainPanel.SetBackgroundColour('#ffffff')

        self.mainBox = wx.BoxSizer(wx.HORIZONTAL)
        self.mainBox.Add(self.sidebar)
        self.mainBox.Add(self.mainPanel, wx.ID_ANY)
        self.panel.SetSizer(self.mainBox)

        self.sidebarBox = wx.BoxSizer(wx.VERTICAL)

        self.startPanelButtonIcon = wx.Image(
            'images/start.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.startPanelButton = wx.BitmapButton(
            self.sidebar, wx.ID_ANY, self.startPanelButtonIcon)
        self.sidebarBox.Add(self.startPanelButton, wx.ALL)

        self.resultPanelButtonIcon = wx.Image(
            'images/result.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.resultPanelButton = wx.BitmapButton(
            self.sidebar, wx.ID_ANY, self.resultPanelButtonIcon)
        self.sidebarBox.Add(self.resultPanelButton, wx.ALL)

        self.graphPanelButtonIcon = wx.Image(
            'images/bar-chart.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.graphPanelButton = wx.BitmapButton(
            self.sidebar, wx.ID_ANY, self.graphPanelButtonIcon)
        self.sidebarBox.Add(self.graphPanelButton, wx.ALL)

        self.sidebar.SetSizer(self.sidebarBox)

        self.startPanel = wx.Panel(self.mainPanel, size=(700, 500))
        self.resultPanel = wx.Panel(self.mainPanel, size=(700, 500))
        self.graphPanel = wx.Panel(self.mainPanel, size=(700, 500))
        self.resultPanel.Hide()
        self.graphPanel.Hide()

        self.startPanelButton.Bind(
            wx.EVT_BUTTON, self.onStartPanelButtonClicked)
        self.resultPanelButton.Bind(
            wx.EVT_BUTTON, self.onResultPanelButtonClicked)
        self.graphPanelButton.Bind(
            wx.EVT_BUTTON, self.onGraphPanelButtonClicked)

        self.initStartPanel()



    def onStartPanelButtonClicked(self, event):
        self.startPanel.Show()
        self.resultPanel.Hide()
        self.graphPanel.Hide()

    def onResultPanelButtonClicked(self, event):
        self.initResultPanel()
        self.resultPanel.Show()
        self.startPanel.Hide()
        self.graphPanel.Hide()

    def onGraphPanelButtonClicked(self, event):
        self.initGraphPanel()
        self.graphPanel.Show()
        self.startPanel.Hide()
        self.resultPanel.Hide()

    def OnclickInput(self,event):
        point = self.text_input.GetValue()
        sendUtils.c_point(self.sock,point,self.playername,self.roomname)
        self.hideInput()
        self.label_waitothers.Show()
        result_thread = threading.Thread(target=self.getResult,args=(self.sock,))
        result_thread.start()

    def OnclickReturn(self,event):
        self.text_wait.SetLabel('五秒后回到输入')
        self.showInputAgain()
        self.updateFrame(1)
        self.bt_return.Hide()
        self.all_input={}
        self.all_score={}
        self.initGraphPanel()
        self.initResultPanel()

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

    def showInputAgain(self):
        self.text_input.SetValue('')
        self.showInput()
        self.hideResult()

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
                self.all_input = jsdata['all_input']
                self.all_score = jsdata['all_score']
                print(self.all_input,self.all_score)
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

import wx
import math
import pymysql

class Player:
    def __init__(self,name = '',score = 100,game_id = -1):
        self.name = name
        self.score = score
        self.game_id = game_id
    def setName(self,name):
        self.name = name
    def getName(self):
        return self.name
    def setScore(self,score):
        self.score = score
    def getScore(self):
        return self.score
    def setGame_id(self,game_id):
        self.game_id=game_id
    def getGame_id(self):
        return self.game_id
    def changeScore(self,bias):
        self.score += bias
# class PlayerGroup:
#     def __init__(self,player_num = 0):
#         self.player_group = []
#         for i in range(player_num):
#             self.player_group.append(Player())
class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='黄金点数游戏',size = (450,300))
        #### 游戏数据
        self.initData()
        #### 组件
        self.initWidgets()
        #### 绑定事件
        self.bindEvents()

    def onClickStrtButton(self,event):
        self.strt_btn.Hide()
        self.ctnu_btn.Show()
        self.show_btn.Show()
        self.exit_btn.Show()
        self.player_numText.Show()
        self.player_numTxcl.Show()
        self.pncm_btn.Show()
        print("hello world")
    def onClickCtnuButton(self,event):
        self.minId = self.maxId = -1
        self.player_input = []
        self.tmpId = 0
        self.inputTxcl.SetValue('')
        # self.inputNotice = "请玩家'" + str(self.tmpId) + "'输入"
        self.inputNotice = "请玩家 " + self.player_group[self.tmpId].getName() + " 输入"
        self.inputText.SetLabel(self.inputNotice)
        self.inputText.Show()
        self.input_btn.Show()
        self.inputTxcl.Show()
        self.batchText.Hide()
        self.scoreText.Hide()
    def onClickShowButton(self,event):
        self.batchText.Hide()
        for i,player in enumerate(self.player_group):
            # self.player_scoreString += "玩家"+str(i+1)+"的分数是"+str(player.getScore())+"\n"
            self.player_scoreString += "玩家" + player.getName()+ "的分数是" + str(player.getScore()) + "\n"
        self.scoreText.SetLabel(self.player_scoreString)
        self.scoreText.Show()
        self.player_scoreString = ""
    def onClickExitButton(self,event):
        sql_insert = 'insert into goldennum values(%s,%s,%s)'
        for i in range(self.player_num):
            player = self.player_group[i]
            args = [player.getName(),player.getScore(),self.game_id]
            self.cursor.execute(sql_insert,args)
        self.conn.commit()
        self.conn.close()
        print('exit')
        self.Destroy()
    def getInputPlayerNum(self,event):
        self.player_num = int(self.player_numTxcl.GetValue())
    def onClickpncmButton(self,event):
        self.player_numText.Hide()
        self.player_numTxcl.Hide()
        self.pncm_btn.Hide()
        for i in range(self.player_num-1):
            self.player_group.append(Player(str(i+1)))
            # self.player_score.append(100)
        self.inputText.Show()
        self.input_nameText.Show()
        self.input_nameTxcl.Show()
        self.input_btn.Show()
        self.inputTxcl.Show()

    def onClickInputButton(self,event):
        self.player_input.append(eval(self.inputTxcl.GetValue()))
        print(self.player_input)
        if(self.firstGame):
            self.player_group[self.tmpId].setName(self.input_nameTxcl.GetValue())
        self.tmpId += 1
        if(self.tmpId>=self.player_num): #输入完了
            self.firstGame=False
            print(len(self.player_group))
            self.golden_score = sum(self.player_input)/self.player_num*0.618
            disList = [math.fabs(x-self.golden_score) for x in self.player_input]
            mx = -1.0
            mn = 110.0
            for i,x in enumerate(disList):
                if x>mx:
                    self.maxId = i
                    mx = x
                if x<mn:
                    self.minId = i
                    mn = x
            self.player_group[self.minId].changeScore(self.player_num)
            self.player_group[self.maxId].changeScore(-2)
            # self.player_score[self.minId] += self.player_num
            # self.player_score[self.maxId] -= 2
            self.inputTxcl.Hide()
            self.inputText.Hide()
            self.input_nameTxcl.Hide()
            self.input_nameText.Hide()
            self.input_btn.Hide()
            # self.batchString = "这局游戏的黄金点数是'" + str(self.golden_score) + "'\n最近的玩家是'" + str(
            #     self.minId+1) + "'\n最远的玩家是'" + str(self.maxId+1) + "'"
            self.batchString = "这局游戏的黄金点数是 " + str(self.golden_score) + "\n最近的玩家是" + self.player_group[self.minId].getName()\
                               + "\n最远的玩家是" + self.player_group[self.maxId].getName()
            self.batchText.SetLabel(self.batchString)
            self.batchText.Show()
            return
        self.inputTxcl.SetValue('')
        self.inputNotice = "请玩家 " + self.player_group[self.tmpId].getName() + " 输入"
        self.inputText.SetLabel(self.inputNotice)

        if(self.firstGame):
            self.input_nameTxcl.SetValue('')
        self.input_nameNotice = "请玩家 " + self.player_group[self.tmpId].getName() + " 输入姓名"
        self.input_nameText.SetLabel(self.input_nameNotice)


    def initWidgets(self):
        panel = wx.Panel(self)
        self.txt = wx.StaticText(panel,-1,label = 'hello world',pos=(10,10))
        self.txt.Hide()
        # self.txt1 = wx.StaticText(panel, -1, label='hello world', pos=(10, 10))
        self.strt_btn = wx.Button(panel, label='开始游戏', pos=(200, 125))
        self.ctnu_btn = wx.Button(panel,label = '继续游戏',pos = (30,220))
        self.show_btn = wx.Button(panel,label = '显示分数',pos = (180,220))
        self.exit_btn = wx.Button(panel,label = '结束游戏',pos = (320,220))
        self.ctnu_btn.Hide()
        self.show_btn.Hide()
        self.exit_btn.Hide()

        self.player_numText = wx.StaticText(panel,-1,label='请输入玩家人数',pos=(10,70),size=(-1,-1))
        self.player_numTxcl = wx.TextCtrl(panel,-1,value='',pos=(120,70),size = (100,20))
        self.pncm_btn = wx.Button(panel,label = '确定',pos = (240,70),size=(60,20))
        self.player_numText.Hide()
        self.player_numTxcl.Hide()
        self.pncm_btn.Hide()

        self.inputNotice = "请玩家 " + self.player_group[self.tmpId].getName() + " 输入"
        self.input_nameNotice = "请玩家 " + self.player_group[self.tmpId].getName() + " 输入姓名"
        self.inputText = wx.StaticText(panel,-1,label=self.inputNotice,pos=(10,70),size=(-1,-1))
        self.input_nameText = wx.StaticText(panel, -1, label=self.input_nameNotice, pos=(10, 120), size=(-1, -1))
        self.inputTxcl = wx.TextCtrl(panel,-1,value='',pos=(120,70),size = (100,20))
        self.input_nameTxcl = wx.TextCtrl(panel,-1,value='',pos=(120,120),size = (100,20))
        self.input_btn =  wx.Button(panel,label = '确定',pos = (240,70),size=(60,20))
        self.inputText.Hide()
        self.input_nameText.Hide()
        self.input_btn.Hide()
        self.inputTxcl.Hide()
        self.input_nameTxcl.Hide()
        self.batchString = "这局游戏的黄金点数是 " + str(self.golden_score) + "\n最近的玩家是" + self.player_group[self.minId].getName() \
                           + "\n最远的玩家是" + self.player_group[self.maxId].getName()
        self.batchText = wx.StaticText(panel,-1,label='',pos=(10,70),size=(-1,-1))
        self.batchText.Hide()

        self.player_scoreString = ""
        self.scoreText = wx.StaticText(panel,-1,label='',pos=(10,70),size=(-1,-1))
        self.scoreText.Hide()

    def bindEvents(self):
        self.strt_btn.Bind(wx.EVT_BUTTON,self.onClickStrtButton)
        self.exit_btn.Bind(wx.EVT_BUTTON,self.onClickExitButton)
        self.player_numTxcl.Bind(wx.EVT_TEXT,self.getInputPlayerNum)
        self.pncm_btn.Bind(wx.EVT_BUTTON,self.onClickpncmButton)
        self.input_btn.Bind(wx.EVT_BUTTON or wx.EVT_TEXT_ENTER,self.onClickInputButton)
        self.ctnu_btn.Bind(wx.EVT_BUTTON,self.onClickCtnuButton)
        self.show_btn.Bind(wx.EVT_BUTTON,self.onClickShowButton)
        self.Show()

    def initData(self):
        self.player_num = 0
        self.golden_score = 0
        self.player_group = []
        self.player_input = []
        self.tmpId = 0
        self.maxId = -1
        self.minId = -1
        self.player_group.append(Player(str(0)))
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

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
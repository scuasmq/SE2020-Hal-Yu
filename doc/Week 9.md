# Week 9-10

[TOC]

### 项目进展

目前已经实现了黄金点游戏的基本功能，GUI用户界面也开发完成，但目前软件仅仅为本地客户端，接下来将进行GUI界面的优化，并实现C/S的运行模式。

### 代码分析

#### 导入库

程序用python语言实现，用wxpython进行GUI设计

```
import wx
import math
from main import *
```

首先，创建一个wx.Frame对象。 wx.Frame 是重要的容器widget。  wx.Frame类是其他widget的父类。 它本身没有父类。  为层次结构中的顶级widget。 创建wx.Frame小部件之后，必须调用Show()方法才能在屏幕上实际显示。

```python
class MyFrame(wx.Frame):
```

#### 应用程序初始化

```python
	def __init__(self):
        super().__init__(parent=None, title='黄金点数游戏',size = (450,300))
        #### 游戏数据
        self.player_num = 0
        self.golen_score = 0
        self.player_score = []
        self.player_input = []
        self.tmpId = 1
        self.maxId = -1
        self.minId = -1
        #### 组件
        panel = wx.Panel(self)
        self.txt = TransparentStaticText(panel,-1,label = 'hello world',pos=(10,10))
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

        self.inputNotice = "请玩家'"+str(self.tmpId)+"'输入"
        self.inputText = wx.StaticText(panel,-1,label=self.inputNotice,pos=(10,70),size=(-1,-1))
        self.inputTxcl = wx.TextCtrl(panel,-1,value='',pos=(120,70),size = (100,20))
        self.input_btn =  wx.Button(panel,label = '确定',pos = (240,70),size=(60,20))
        self.inputText.Hide()
        self.input_btn.Hide()
        self.inputTxcl.Hide()

        self.batchString = "这局游戏的黄金点数是'"+str(self.golen_score)+"'\n最近的玩家是'"+str(self.minId)+"'\n最远的玩家是'"+str(self.maxId)+"'"
        self.batchText = wx.StaticText(panel,-1,label='',pos=(10,70),size=(-1,-1))
        self.batchText.Hide()

        self.player_scoreString = ""
        self.scoreText = wx.StaticText(panel,-1,label='',pos=(10,70),size=(-1,-1))
        self.scoreText.Hide()
        #### 绑定事件
        self.strt_btn.Bind(wx.EVT_BUTTON,self.onClickStrtButton)
        self.exit_btn.Bind(wx.EVT_BUTTON,self.onClickExitButton)
        self.player_numTxcl.Bind(wx.EVT_TEXT,self.getInputPlayerNum)
        self.pncm_btn.Bind(wx.EVT_BUTTON,self.onClickpncmButton)
        self.input_btn.Bind(wx.EVT_BUTTON,self.onClickInputButton)
        self.ctnu_btn.Bind(wx.EVT_BUTTON,self.onClickCtnuButton)
        self.show_btn.Bind(wx.EVT_BUTTON,self.onClickShowButton)
        self.Show()
```

#### “开始游戏”按钮被点击的事件处理函数

```python
	def onClickStrtButton(self,event):
        self.strt_btn.Hide()
        self.ctnu_btn.Show()
        self.show_btn.Show()
        self.exit_btn.Show()
        self.player_numText.Show()
        self.player_numTxcl.Show()
        self.pncm_btn.Show()
        # print("hello world")
```

#### “继续游戏”按钮被点击的事件处理函数

```python
    def onClickCtnuButton(self,event):
        self.minId = self.maxId = -1
        self.player_input = []
        self.tmpId = 1
        self.inputTxcl.SetValue('')
        self.inputNotice = "请玩家'" + str(self.tmpId) + "'输入"
        self.inputText.SetLabel(self.inputNotice)
        self.inputText.Show()
        self.input_btn.Show()
        self.inputTxcl.Show()
        self.batchText.Hide()
        self.scoreText.Hide()
```

#### “显示结果”

```python
    def onClickShowButton(self,event):
        self.batchText.Hide()
        for i,score in enumerate(self.player_score):
            self.player_scoreString += "玩家'"+str(i+1)+"'的分数是'"+str(score)+"'\n"
        self.scoreText.SetLabel(self.player_scoreString)
        self.scoreText.Show()
        self.player_scoreString = ""
```

#### “退出游戏”

```python
    def onClickExitButton(self,event):
        print('exit')
        self.Destroy()
```

#### 输入参与游戏的总人数

```python
    def getInputPlayerNum(self,event):
        self.player_num = int(self.player_numTxcl.GetValue())
        # print(self.player_num)
        pass
```

#### 点击“确定”按钮，读取当前玩家输入

```python
    def onClickpncmButton(self,event):
        self.player_numText.Hide()
        self.player_numTxcl.Hide()
        self.pncm_btn.Hide()
        for i in range(self.player_num):
            self.player_score.append(100)
        self.inputText.Show()
        self.input_btn.Show()
        self.inputTxcl.Show()
```

#### 读取玩家输入，若全部完成则显示游戏结果

```python
    def onClickInputButton(self,event):
        self.player_input.append(int(self.inputTxcl.GetValue()))
        print(self.player_input)
        self.tmpId += 1

        if (self.tmpId > self.player_num): #输入完了
            self.golen_score = sum(self.player_input)/self.player_num*0.618
            disList = [math.fabs(x-self.golen_score) for x in self.player_input]
            mx = -1.0
            mn = 110.0
            for i,x in enumerate(disList):
                if x>mx:
                    self.maxId = i
                    mx = x
                if x<mn:
                    self.minId = i
                    mn = x
            self.player_score[self.minId] += self.player_num
            self.player_score[self.maxId] -= 2
            print(self.golen_score)
            print(self.player_score)
            self.inputTxcl.Hide()
            self.inputText.Hide()
            self.input_btn.Hide()
            self.batchString = "这局游戏的黄金点数是'" + str(self.golen_score) + "'\n最近的玩家是'" + str(
                self.minId+1) + "'\n最远的玩家是'" + str(self.maxId+1) + "'"
            self.batchText.SetLabel(self.batchString)
            self.batchText.Show()
            return
        self.inputTxcl.SetValue('')
        self.inputNotice = "请玩家'" + str(self.tmpId) + "'输入"
        self.inputText.SetLabel(self.inputNotice)
```

#### 若为直接调用，则运行程序

```python
if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
```



### 参考文档

wxPython tutorial  http://zetcode.com/wxpython/
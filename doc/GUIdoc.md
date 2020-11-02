

```
wx.TextCtrl(self.panel,-1,value='',pos=(10,10),size=(100,30))
TextCtrl.GetValue() 获得值

self.Bind(wx.EVT_TEXT,self.OnEnter,self.text) 绑定事件
```



```
wx.StaticText(self.panel, -1,label='123',pos=(10,70),size=(-1,-1))
SetLabel('xxx')
Hide()
Show()
```
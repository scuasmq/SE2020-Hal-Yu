import wx

class Example(wx.Frame):
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title, size = (750, 500))

        self.InitUI()
        self.Centre()

    def InitUI(self):

        # panel = wx.Panel(self)
        # panel.SetBackgroundColour('#4f5049')
        
        # midPan = wx.Panel(panel)
        # midPan.SetBackgroundColour('#ededed')

        # vbox = wx.BoxSizer(wx.VERTICAL)
        # vbox.Add(midPan, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)
        
        # panel.SetSizer(vbox)

        # screenSize = wx.DisplaySize()
        
        # toolBar = self.CreateToolBar(wx.TB_VERTICAL|wx.TB_TEXT)
        
        # ctool = toolBar.AddTool(wx.ID_ANY, 'Start', wx.Bitmap('C:/Users/vince/Pictures/start.png'))
        # atool = toolBar.AddTool(wx.ID_ANY, 'Result', wx.Bitmap('C:/Users/vince/Pictures/chart.png'))
        # btool = toolBar.AddTool(wx.ID_ANY, 'Chart', wx.Bitmap('C:/Users/vince/Pictures/chart.png'))
        # toolBar.Realize()
        
        # self.SetTitle('Simple toolbar')
        # self.Centre()

        panel = wx.Panel(self)
        # panel.SetBackgroundColour('#dddddd')

        sidebar = wx.Panel(panel, size = (64, 600))
        # sidebar.SetBackgroundColour('#ffffff')
        
        mainPanel = wx.Panel(panel, size = (700, 600))
        # mainPanel.SetBackgroundColour('#ffffff')
        
        mainBox = wx.BoxSizer(wx.HORIZONTAL)
        mainBox.Add(sidebar)
        mainBox.Add(mainPanel, wx.ID_ANY)
        panel.SetSizer(mainBox)

        sidebarBox = wx.BoxSizer(wx.VERTICAL)
        
        startPanelButtonIcon = wx.Image('./static/img/start.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.startPanelButton = wx.BitmapButton(sidebar, wx.ID_ANY, startPanelButtonIcon)
        sidebarBox.Add(self.startPanelButton, wx.ALL)

        resultPanelButtonIcon = wx.Image('./static/img/result.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.resultPanelButton = wx.BitmapButton(sidebar, wx.ID_ANY, resultPanelButtonIcon)
        sidebarBox.Add(self.resultPanelButton, wx.ALL)

        graphPanelButtonIcon = wx.Image('./static/img/bar-chart.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.graphPanelButton = wx.BitmapButton(sidebar, wx.ID_ANY, graphPanelButtonIcon)
        sidebarBox.Add(self.graphPanelButton, wx.ALL)
        
        sidebar.SetSizer(sidebarBox)

        self.startPanel = wx.Panel(mainPanel, size = (700, 500))
        self.startPanel.SetBackgroundColour('#ffffff')
        self.resultPanel = wx.Panel(mainPanel, size = (700, 500))
        self.resultPanel.SetBackgroundColour('#ffffff')
        self.graphPanel = wx.Panel(mainPanel, size = (700, 500))
        self.graphPanel.SetBackgroundColour('#ffffff')
        self.resultPanel.Hide()
        self.graphPanel.Hide()
        
        start_btn = wx.Button(self.startPanel, label='开始游戏', pos = (200, 125))
        continue_btn = wx.Button(self.startPanel, label = '继续游戏', pos = (30,220))
        show_btn = wx.Button(self.startPanel, label = '显示分数', pos = (180,220))
        exit_btn = wx.Button(self.startPanel, label = '结束游戏', pos = (320,220))

        self.startPanelButton.Bind(wx.EVT_BUTTON, self.onStartPanelButtonClicked)
        self.resultPanelButton.Bind(wx.EVT_BUTTON, self.onresultPanelButtonClicked)
        self.graphPanelButton.Bind(wx.EVT_BUTTON, self.ongraphPanelButtonClicked)
    
    def onStartPanelButtonClicked(self, event):
        self.startPanel.Show()
        self.resultPanel.Hide()
        self.graphPanel.Hide()
    def onresultPanelButtonClicked(self, event):
        self.resultPanel.Show()
        self.startPanel.Hide()
        self.graphPanel.Hide()
    def ongraphPanelButtonClicked(self, event):
        self.graphPanel.Show()
        self.startPanel.Hide()
        self.resultPanel.Hide()
    
        
def main():
    app = wx.App()
    ex = Example(None, title='Border')
    ex.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
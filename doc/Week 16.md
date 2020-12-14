# Week 16

### 显示表格

该部分功能由wx.grid实现，注意需要提前导入wx.grid，接着用SetCellValue函数即可修改表格数据

```python
import wx.grid

	def initResultPanel(self):
        length = len(self.all_input)

        self.resultGrid = wx.grid.Grid(self.resultPanel, -1, size=(325, 400), pos=(20, 20))
        self.resultGrid.CreateGrid(length, 3)
        self.resultGrid.SetColLabelValue(0, "用户名")
        self.resultGrid.SetColLabelValue(1, "输入")
        self.resultGrid.SetColLabelValue(2, "得分")
        for i,(name,input) in enumerate(self.all_input.items()):
            self.resultGrid.SetCellValue(i, 0, name)
            self.resultGrid.SetCellValue(i, 1, str(input))
            self.resultGrid.SetCellValue(i, 2, str(self.all_score[name]))
```



### 显示直方图

##### matplotlib.pyplib

matplotlib.pyplot是使matplotlib像MATLAB一样工作的函数的集合。 每个pyplot函数都会对图形进行一些更改：例如，创建图形，在图形中创建绘图区域，在绘图区域中绘制一些线条，用标签装饰绘图等。

在matplotlib.pyplot中，跨函数调用保留各种状态，以便跟踪当前图形和绘图区域之类的东西，并将绘图函数定向到当前轴（请注意，此处和大多数位置的“轴” 该文档指的是图形的轴部分，而不是多个轴的严格数学术语。

使用plt绘图时，调用plt.show()会打开一个画板，若将其关闭，则之前所有的数据将被清空，再次调用plt.show()什么也不会发生

但是如果不调用plt.show()，则之前绘制的所有信息都会保存下来，在下次show的时候显示。程序中出现bug的原因就是只调用了plt.savefig，之前的数据依然存在，所以显示的结果不正确，也可以在每次绘图之前调用plt.cla()，即可清空画布。

```python
    def initGraphPanel(self):
        inputs = list(self.all_input.values())

        group = range(0, 101, 1)
        plt.cla()
        plt.hist(inputs, group, rwidth=0.8)
        plt.grid(alpha=0.3)
        plt.savefig('images/hist.jpg')

        self.img = wx.Image('images/hist.jpg', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.bitmapGraph = wx.StaticBitmap(self.graphPanel, -1, self.img, (0, 0))

        self.bitmapGraph.Show()
```

如上所示为程序的数据可视化部分，获取每轮游戏的所有用户输入，然后以直方图的形式绘制在面板上。由于直接在wxpython中调用matplotlib绘制直方图不方便，所以采用的解决方案是，直接调用matplotlib绘图并将其保存下来，再将图片置于面板中。

显示
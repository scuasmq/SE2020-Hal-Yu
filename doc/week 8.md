# 黄金点游戏 Week 7-8

## 课设要求

分组编写一个满足下列要求的黄金点游戏程序。

- 游戏规则： N 个同学（ N 通常大于 10 ），每人写一个 0~100 之间的有理数
  不包括 0 或 100)，交给裁判，裁判算出所有数字的平均值，然后乘以 0.618
  所谓黄金分割常数），得到 G 值。提交的数字最靠近 G （取绝对值）的同
  学得到 N 分，离 G 最远的同学得到－ 2 分，其他同学得 0 分。

- 采用单机方式实现，需要为用户提供便利的输入界面。
- 该游戏每次至少可以运行 10 轮以上，并能够保留各轮比赛结果。
- 后续在此基础上迭代开发。



## 程序设计

为了方便之后的迭代开发，采用面向对象的设计思想

### 定义一个玩家类，保存每个玩家的信息

```python
class Player():
    def __init__(self,id):
        self.id = id
        self.score = 100
        self.num = 0
    def getNum(self):
        self.num = float(input('玩家·{}·输入数字:'.format(self.id)))
    def changeScore(self,bias = 0):
        self.score+=bias
    def getScore(self):
        return self.score
    def getId(self):
        return self.id
```



### 定义了计分板来控制游戏和显示分数

```python
class ScoreBoard():
    def __init__(self):
        self.golenScore = -1;
        self.getGameeController()
        self.switch = {'case0':self.case0,
                       'case1':self.case1,
                       'case2':self.case2,
                       'case3':self.case3,}

    def initPlayers(self):
        self.playerNum = int(input('请输入玩家数量\n'))
        self.Players = [Player(i+1) for i in range(self.playerNum)]
        self.getPlayersNum()
        self.countScore()
    def showScore(self):
        for player in self.Players:
            print('player'+str(player.id)+'\'s score is '+str(player.getScore()))

    def showNotice(self):
        print("------------")
        print("按·1·开始游戏")
        print("按·2·继续游戏")
        print("按·3·显示分数")
        print("按·0·结束游戏")
    def getGameeController(self):
        self.showNotice()
        self.gameController = int(input())

    def getPlayersNum(self): #获取玩家的输入
        for player in self.Players:
            player.getNum()

    def countScore(self): #计算玩家的分数
        numList = [p.num for p in self.Players]
        sumScore = sum(numList)
        self.goldenScore = sumScore*0.618/self.playerNum
        disList = [math.fabs(x-self.goldenScore) for x in numList]
        mx = -1.0
        mn = 110.0
        indexOfMin = -1
        indexOfMax = -1
        for i,x in enumerate(disList):
            if x>mx:
                indexOfMax = i
                mx = x
            if x<mn:
                indexOfMin = i
                mn = x

        self.Players[indexOfMin].changeScore(self.playerNum)
        self.Players[indexOfMax].changeScore(-2)

    def getGoldenScore(self):
        return self.golenScore

```



### 为了程序结构的清晰，在ScoreBoard类里实现了switch语句

```python
    # 这里是实现switch语句
    def case0(self):
        return
    def case1(self):
        return
    def case2(self):
        self.getPlayersNum()
        self.countScore()
    def case3(self):
        self.showScore()
    def default(self):
        print('非法输入，请重新输入选项')
    def Switch(self,case):
        case = 'case'+str(case)
        self.switch.get(case,self.default)()
```



## 结对编程的感悟

- 结对编程可以缩短debug时间，更快地想出解决方案

  在寻找indexOfMin和Max的时候，一开始是用的list.index(max(list(element)))这样的方法但是程序崩溃了

  但是领航员很快地发现了这个问题是由浮点数精度比较导致的，并且很快提出了解决的方法

### 结对编程的好处

  1、**互相鼓励，不容易沮丧**：团队工作能增加成员的工作积极性。因为在面对问题的时候，会有人一起分担，共同尝试新的策略。

  2、**互相监督，不容易偷懒**：两个人一起工作需要互相配合，如果想偷懒去干别的，就会拖延工作进度。

  3、**互相学习编程技巧**：在编程中，相互讨论，可以更快更有效地解决问题，互相请教对方，可以得z到能力上的互补。

  4、**可以培养和训练新人**：让资深开发者和新手一起工作，可以让新人更快上手。

  5、**多双眼睛，少点 bug**：两人互相监督工作，可以增强代码和产品质量，并有效的减少 BUG。
import math
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

class ScoreBoard():
    def __init__(self):
        self.golenScore = -1
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
        print('golenScore is '+str(self.getGoldenScore()))
    def getGoldenScore(self):
        return self.goldenScore

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

if __name__ == '__main__':
    print('### WELCOME TO THE GOLDEN EXPERIENCE ###')
    mainBoard = ScoreBoard()
    while mainBoard.gameController>0:
        if not hasattr(mainBoard,'Players'):
            mainBoard.initPlayers()
        elif mainBoard.gameController ==1:
            print('游戏已经开始，请重新输入选项')
            mainBoard.getGameeController()
            continue
        mainBoard.getGameeController()
        mainBoard.Switch(mainBoard.gameController)
    print('### WAIT YOUR NEXT PLAY ###')
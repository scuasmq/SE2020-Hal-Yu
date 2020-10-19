

class Player():
    def __init__(self,id):
        self.id = id
        self.score = 100
    pass

class oneGame():
    def __init__(self,Players):
        self.Players = Players

    def countScore(self):
        pass

    def getInput(self):
        self.countScore()

class ScoreBoard():
    def __init__(self,Players):
        self.Players = Player

    def showScore(self):
        for player in self.Players:
            print('player'+str(player.id)+'\'s score is '+str(self.score))


if __name__ == '__main__':
    print("------------")
    print("按·1·开始游戏")
    print("按·2·继续游戏")
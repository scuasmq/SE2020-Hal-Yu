from frames import roomFrame, loginFrame, gameFrame

class guiManager():
    def __init__(self,updateFrame,sock):
        self.updateFrame = updateFrame
        self.sock = sock
        self.frameDict = {}

    def getFrame(self,type,roomname=None,gameid=None,playername=None):
        frame = self.frameDict.get(type)
        if frame is None:
            frame = self.createFrame(type,self.sock,roomname,gameid,playername)
            self.frameDict[type] = frame
        if(type==2):
            frame.setRoomName(roomname)
            print('setRoomName')
        return frame

    def createFrame(self,type,sock,roomname=None,gameid=None,playername=None):
        if type==0:
            return loginFrame.LoginFrame(self.sock, parent=None, id=type, updateFrame = self.updateFrame)
        if type==1:
            return roomFrame.RoomFrame(self.sock, parent=None, id=type, updateFrame=self.updateFrame)
        if type==2:
            return gameFrame.GameFrame(self.sock,roomname,gameid,playername, parent=None, id=type, updateFrame=self.updateFrame)
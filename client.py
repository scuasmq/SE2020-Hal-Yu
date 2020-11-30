import wx
import socket
from Utils import guiManager as FrameManager

sock = socket.socket()
host = 'localhost'
port = 12346
addr = (host,port)
sock.connect(addr)

def jsonParse(js):
    recjs = eval(js)
    if recjs['MESSAGE'] == 'SUCCESS':
        return True

data = ''

def recvMsg():
    while True:
        try:
            data = sock.recv(1024)
        except:
            continue
        else:
            jsonParse(data)
        # time.sleep(0.5)
        # print('in thread')

class clientApp(wx.App):
    def OnInit(self):
        self.manager = FrameManager.guiManager(self.updateFrame,sock)
        # self.frame = loginFrame.LoginFrame(sock)
        self.frame = self.manager.getFrame(0)
        self.SetTopWindow(self.frame)
        self.frame.Show(True)
        return True
    def OnExit(self):
        sock.close()

    def updateFrame(self, type,roomname=None,gameid=None,playername=None):
        self.frame.Show(False)
        self.frame = self.manager.getFrame(type,roomname,gameid,playername)
        self.SetTopWindow(self.frame)
        self.frame.Show(True)


if __name__ == "__main__":
    # recvThread = threading.Thread(target=recvMsg,args=())
    # recvThread.start()
    app = clientApp()
    app.MainLoop()

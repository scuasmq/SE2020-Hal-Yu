json = {}

def message(soc,string):
    json = {'OPERATION':'message',
            'MESSAGE':''}
    json['MESSAGE'] = string
    soc.sendall(str.encode(str(json)))

def s_loginSuccess(soc):
    json = {'OPERATION':'login',
            'MESSAGE':'success'}
    soc.sendall(str.encode(str(json)))

def s_loginFailure(soc):
    json = {'OPERATION':'login',
            'MESSAGE':'failure'}
    soc.sendall(str.encode(str(json)))

def c_sendLogInfo(soc,username,password):
    json = {'OPERATION':'login',
            'username':username,
            'password':password}
    print(username,password)
    soc.sendall(str.encode(str(json)))

def c_sendRegisterInfo(soc,username,password):
    json = {'OPERATION':'register',
            'username':username,
            'password':password}
    soc.sendall(str.encode((str(json))))

def s_registerFailure(soc):
    json = {'OPERATION':'register',
            'MESSAGE':'failure'}
    soc.sendall(str.encode(str(json)))

def s_registerSuccess(soc):
    json = {'OPERATION':'register',
            'MESSAGE':'success'}
    soc.sendall(str.encode(str(json)))

def c_getUsername(soc):
    json = {'OPERATION':'username',
            'MESSAGE':'get'}
    soc.sendall(str.encode(str(json)))
def s_sendUsername(soc,username):
    json = {'OPERATION':'username',
            'MESSAGE':username}
    soc.sendall(str.encode(str(json)))

def c_enterRoom(soc,roomname,playername):
    json = {'OPERATION':'enter',
            'roomname':roomname,
            'playername':playername}
    soc.sendall(str.encode(str(json)))
def s_enterSuccess(soc,gameid,playerid):
    json = {'OPERTAION':'enter',
            'MESSAGE':'success',
            'gameid':gameid,
            'playerid':playerid}
    soc.sendall(str.encode(str(json)))
def s_enterFailure(soc):
    json = {'OPERTAION':'enter',
            'MESSAGE':'failure'}
    soc.sendall(str.encode(str(json)))

def c_createRoom(soc,roomname,maxnum,playername,epoch):
    json = {'OPERATION':'create',
            'roomname':roomname,
            'maxnum':maxnum,
            'epoch':epoch,
            'playername':playername}
    soc.sendall(str.encode(str(json)))

def s_createSuccess(soc,gameid):
    json = {'OPERTAION':'create',
            'MESSAGE':'success',
            'gameid':gameid}
    soc.sendall(str.encode(str(json)))
def s_createFailure(soc):
    json = {'OPERTAION':'create',
            'MESSAGE':'failure'}
    soc.sendall(str.encode(str(json)))
def c_readyQuery(soc,roomname):
    json = {'OPERATION':'ready',
            'roomname':roomname}
    soc.sendall(str.encode(str(json)))
def s_readyOK(soc):
    json = {'OPERATION':'ready',
            'MESSAGE':'OK'}
    soc.sendall(str.encode(str(json)))
def s_readyNOTOK(soc):
    json = {'OPERATION':'ready',
            'MESSAGE':'NOTOK'}
    soc.sendall(str.encode(str(json)))

def c_point(soc,input,playername,roomname):
    json = {'OPERATION':'input',
            'input':input,
            'playername':playername,
            'roomname': roomname}
    soc.sendall(str.encode(str(json)))

def c_resultQuery(soc,playername,roomname):
    json = {'OPERATION': 'result',
            'playername':playername,
            'roomname':roomname}
    soc.sendall(str.encode(str(json)))

def s_result(soc,result,end,ok,all_input,all_score):
    json = {'OPERATION':'result',
            'MESSAGE':ok,
            'result':result,
            'end':end,
            'all_input':all_input,
            'all_score':all_score}
    soc.sendall(str.encode(str(json)))
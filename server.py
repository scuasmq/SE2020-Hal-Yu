import socket
import threading
import pymysql
from Utils import sqlUtils, sendUtils
import math
userSocket = []
roomNum = {}
roomMax = {}
sendResult = {}
Result = {}
room_Score_dict = {}
room_Input_dict = {}
roomCreator = {}
room_result = {}
room_epoch = {}
room_epochCnt = {}
room_responseCnt = {}
room_Goldenscore = {}
roomname_gameid_dict = {}
max_gameid = -1

def s_sqlInit(host = 'localhost',user = 'dataUser',password = 'scusmq61347',database = 'SE2020',charset = 'utf8'):
    global conn,cursor
    conn = pymysql.connect(host=host,user=user,password=password,database=database,charset=charset)
    cursor = conn.cursor()

def s_sqlTest():
    sql = 'select max(game_id) from goldennum'
    cursor.execute(sql)
    global max_gameid
    max_gameid = int(cursor.fetchone()[0])
    max_gameid+=1
    print('max_gameid:',max_gameid)

def s_socketInit(host = 'localhost',port = 12346):
    global sock
    sock= socket.socket()
    s_addr = (host, port)
    sock.bind(s_addr)
    sock.listen(60)

def conn_thread(soc):
    username = ''
    global roomMax,roomMax,max_gameid,room_Score_dict,room_Input_dict,room_responseCnt
    while True:
        data = soc.recv(1024)
        jsData = eval(data)
        operation = jsData['OPERATION']
        if(operation=='login'):
            args = (jsData['username'], jsData['password'])
            sql = "select count(*) from userInfo where username = '%s'and password='%s'"%args
            cursor.execute(sql)
            usernum = cursor.fetchone()[0]
            if(usernum==1):
                username = jsData['username']
                sendUtils.s_loginSuccess(soc)
            else:
                sendUtils.s_loginFailure(soc)

        if(operation=='register'):
            if(sqlUtils.uniqueUsername(conn, jsData['username'])):
                sqlUtils.insertUser(conn, jsData['username'], jsData['password'])
                sendUtils.s_registerSuccess(soc)
            else:
                sendUtils.s_registerFailure(soc)

        if(operation=='username'):
            sendUtils.s_sendUsername(soc,username)

        if(operation=='enter'):
            roomname = jsData['roomname']
            if roomname not in roomNum:
                sendUtils.s_enterFailure(soc)
            elif roomNum[roomname]>=roomMax[roomname]:
                sendUtils.s_enterFailure(soc)
            else:
                sendUtils.s_enterSuccess(soc,max_gameid,roomNum[roomname])
                playerScore = room_Score_dict[roomname]
                roomNum[roomname] += 1
                playerScore[jsData['playername']] = 100

        if(operation=='create'):
            roomname = jsData['roomname']
            maxnum = jsData['maxnum']
            room_Score_dict[roomname] = {}
            room_Input_dict[roomname] = {}
            room_responseCnt[roomname] = 0
            playerScore = room_Score_dict[roomname]
            if roomname in roomMax:
                sendUtils.s_createFailure(soc)
            else:
                roomMax[roomname] = eval(maxnum)
                roomNum[roomname] = 1
                playerScore[jsData['playername']] = 100
                room_epoch[roomname] = jsData['epoch']
                room_epochCnt[roomname] = 0
                roomCreator[roomname] = jsData['playername']
                sendUtils.s_createSuccess(soc,max_gameid)
                roomname_gameid_dict[roomname] = max_gameid
                max_gameid += 1

        if(operation=='ready'):
            roomname = jsData['roomname']
            tmpnum = roomNum[roomname]
            tmpmax = roomMax[roomname]
            if(tmpnum>=tmpmax):
                sendUtils.s_readyOK(soc)
            else:
                sendUtils.s_readyNOTOK(soc)

        if(operation=='input'):
            roomname = jsData['roomname']
            playername = jsData['playername']
            input = eval(jsData['input'])
            playerInput = room_Input_dict[roomname]
            playerInput[playername] = input

        if(operation=='result'):
            roomname = jsData['roomname']
            playername = jsData['playername']
            playerInput = room_Input_dict[roomname]
            playerscore = room_Score_dict[roomname]
            input_num = len(playerInput)
            player_num = roomMax[roomname]
            creator = roomCreator[roomname]
            far_name =''
            near_name = ''
            dis_dict = {}
            max_p = -1
            min_p = 1000
            golden_p = 0
            result_str = ''
            if creator==playername and input_num==player_num:
                print('allInput:',playerInput)
                for name,value in playerInput.items():
                    golden_p+=value
                golden_p /= player_num
                golden_p *=0.618
                for name,value in playerInput.items():
                    dis_dict[name] = math.fabs(value-golden_p)
                for name,dis in dis_dict.items():
                    if dis>max_p:
                        max_p = dis
                        far_name = name
                    if dis<min_p:
                        min_p = dis
                        near_name = name
                playerscore[near_name] += player_num
                playerscore[far_name] -= 2
                for name,score in playerscore.items():
                    result_str += '玩家 '+name+'的分数为:'+str(score)+'\n'
                result_str += '上次的winner是:' + near_name + '\n'
                result_str += '上次的loser是:' + far_name + '\n'
                result_str += '黄金点数是:' + str(golden_p) +'\n'
                room_responseCnt[roomname] = player_num
                room_result[roomname] = result_str
                room_epochCnt[roomname] += 1
                del room_Input_dict[roomname]
                room_Input_dict[roomname] = {}

            if room_responseCnt[roomname]>0:
                result_str = room_result[roomname]
                end = room_epochCnt[roomname]==room_epoch[roomname]
                ok = 'OK'
                sendUtils.s_result(soc,result_str,end,ok)
                room_responseCnt[roomname] -= 1
                if room_epochCnt[roomname]==room_epoch[roomname]:
                    sqlUtils.insertHistory(conn,playername,playerscore[playername],roomname_gameid_dict[roomname])
            else:
                sendUtils.s_result(soc,'',False,'NOTOK')

s_socketInit()
s_sqlInit()
s_sqlTest()

while True:
    c,addr = sock.accept()
    print('连接地址: '+str(addr))
    # Send.s_loginSuccess(c)
    userSocket.append(c)
    handle_thread =  threading.Thread(target=conn_thread,args=(c,))
    handle_thread.start()
    print('ok')

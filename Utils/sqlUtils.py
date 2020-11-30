import pymysql
def uniqueUsername(conn,username):
    sql = "select count(*) from userInfo where username = %s"
    args = [username]
    cursor = conn.cursor()
    cursor.execute(sql,args)
    usernum = cursor.fetchone()[0]
    if(usernum==0):
        return True
    else:
        return False

def insertUser(conn,username,password):
    sql = "insert into userInfo values(%s,%s)"
    args = [username,password]
    cursor = conn.cursor()
    cursor.execute(sql,args)
    conn.commit()
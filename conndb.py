import pymysql
conn = pymysql.connect(host = "localhost",user = "dataUser",password = "scusmq61347",database = "SE2020",charset = "utf8")
cursor =  conn.cursor()
sql = 'select count(*) from goldennum'
cursor.execute(sql)
print(cursor.fetchone())
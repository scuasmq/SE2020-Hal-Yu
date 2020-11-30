import pymysql
conn = pymysql.connect(host = "47.106.229.249",user = "DataUser",password = "123456",database = "SE2020",charset = "utf8")
cursor =  conn.cursor()
sql = 'select count(*) from goldennum'
cursor.execute(sql)
print(cursor.fetchone())
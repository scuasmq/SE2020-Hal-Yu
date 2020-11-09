使用pymysql包,py3.x不支持MySQLdb，不要试图安装！

```
conn = pymysql.connect(host = "localhost",user = "dataUser",password = "scusmq61347",database = "SE2020",charset = "utf8")
cursor = db.cursor() //游标对象
try:
   # 执行sql语句
   cursor.executemany(sql,val)  //此处val是一个二维tuple
   cursor.execute(sql,val)
   # 提交到数据库执行
   db.commit()
except:
   # 如果发生错误则回滚
db.close()
```

多行查询:

```
results = cursor.fetchall()
   for row in results:
   xxx = row[0]
   xxx = row[1]...
cursor.fetchone() //获取单条数据
```


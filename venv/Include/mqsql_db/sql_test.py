import pymysql
from sqlalchemy import Column

# 连接数据库
db = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='password',
    database='world',
    charset='utf8'
    # autocommit = True
)

# 获取游标
cursor = db.cursor()

# 查询
# sql = "SELECT * FROM city WHERE ID in (%s,%s)"
# cursor.execute(sql,(1,2))
# result=cursor.fetchall()
# print(result)
# cursor.close()
# db.close()

# 删除
# sql = "DELETE FROM city WHERE Population<153872"
# cursor.execute(sql)
# print('success')
# # 提交，保存语句
# db.commit()
# cursor.close()
# db.close()

# 更新
# sql = 'UPDATE CITY SET ID =%s WHERE ID in (%s)'
# cursor.execute(sql, ("12", "23"))
# db.commit()
# cursor.close()
# db.close()

# 插入
sql = 'INSERT INTO city(ID,Name,CountryCode,District,Population) VALUES(%s,%s,%s,%s,%s)'
cursor.execute(sql, ('15', 'Dsf', 'ALB', 'des', '7543'))
db.commit()
print('success')
cursor.close()
db.close()

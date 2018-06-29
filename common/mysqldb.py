import mysql.connector
class SQL:
	username = 'root'
	password = 'helloworld'
	database = 'pyspider_resultdb'
	host = '127.0.0.1'
	connection = ''

	def __init__(self):
		self.connect()
	def connect(self):
		config = {
			'user':SQL.username,
			'password':SQL.password,
			'host':SQL.host,
			'database':SQL.database
		}
		SQL.connection = mysql.connector.connect(**config)

	def escape(self,string):
		return '`%s`' % string

	def insert(self,table=None,**results):
		table = self.escape(table)
		if results:
			keys = []
			values = []
			for key,value in results.items():
				keys.append(self.escape(key))
				values.append("'%s'" % value)
			keys = ','.join(keys)
			values = ','.join(values)
			query = "insert into %s (%s) VALUES (%s)" % (table, keys, values)
			cur = SQL.connection.cursor()
			cur.execute(query)
			SQL.connection.commit()

# con=SQL().connection
# cursor = con.cursor(dictionary=True)
# cursor.execute('select * from user')
# datas=cursor.fetchall()
# for data in datas:
# 	print('id:%s,name:%s' % (data['id'],data['name']))
# cursor.close()
# con.close()




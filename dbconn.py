import mysql.connector

class mysql_conn:
	
	def __init__(self):
		self.conn = mysql.connector.connect(user='root', password='', host='127.0.0.1',database='BOOKS')
		self.cursor = self.conn.cursor()

	def getBooks(self):
		query = 'SELECT BOOKS.ID, BOOKS.TITLE, AUTHORS.FULL_NAME, DONE, TYPE FROM BOOKS,AUTHORS WHERE BOOKS.AUTHOR_ID = AUTHORS.ID'
		self.cursor.execute(query)
		res = []
		for (ID,title,author,done,typ) in self.cursor:
			res.append((ID,title,author,done,typ))
		return res
		
		
	def __del__(self):
		self.conn.close()

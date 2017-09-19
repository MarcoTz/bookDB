import mysql.connector

class mysql_conn:
	
	def __init__(self):
		self.conn = mysql.connector.connect(user='root', password='', host='127.0.0.1',database='BOOKS')

	def __del__(self):
		self.conn.close()

	def getBooks(self):
		cursor = self.conn.cursor()
		query = 'SELECT BOOKS.ID, BOOKS.TITLE, AUTHORS.FULL_NAME, DONE, TYPE FROM BOOKS,AUTHORS WHERE BOOKS.AUTHOR_ID = AUTHORS.ID'
		cursor.execute(query)
		res = []
		for (ID,title,author,done,typ) in cursor:
			res.append((ID,title,author,done,typ))
		cursor.close()
		return res
		
			
	def updateTitle(self,book_id,title):
		cursor = self.conn.cursor()
		query = 'UPDATE BOOKS SET TITLE=%s WHERE ID=%s'
		print(book_id)
		print(title)
		cursor.execute(query, (title, book_id))
		self.conn.commit()
		cursor.close()

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
		cursor.execute(query, (title, book_id))
		cursor.close()

	def updateAuthor(self,book_id,author_id):
		cursor = self.conn.cursor()
		query = 'UPDATE BOOKS SET AUTHOR_ID=%s WHERE ID=%s'
		
		cursor.execute(query, (author_id, book_id))
		cursor.close()
	
	def updateDone(self,book_id,done):
		cursor = self.conn.cursor()
		query = 'UPDATE BOOKS SET DONE=%s WHERE ID=%s'
		newDone = ''
		if done:
			newDone = '1'
		else:
			newDone = '0'

		cursor.execute(query, (newDone,book_id))
		cursor.close()
	
	def updateType(self,book_id,typ):
		cursor = self.conn.cursor()
		query = 'UPDATE BOOKS SET TYPE=%s WHERE ID=%s'
		cursor.execute(query, (typ,book_id))
		cursor.close()
		

	def getAuthorId(self,name):
		cursor = self.conn.cursor()
		query = 'SELECT ID FROM AUTHORS WHERE FULL_NAME=%s'
		cursor.execute(query,(name,))
		row = cursor.fetchone()
		cursor.close()
		if row is not None:
			return row[0]
		else:
			return None

	def insertAuthor(self,name):
		cursor = self.conn.cursor()
		query = 'INSERT INTO AUTHORS (FULL_NAME) VALUES (%s)'

		cursor.execute(query,(name,))
		cursor.close()

	def saveChanges(self):
		self.conn.commit()

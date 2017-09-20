import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import re
import dbconn
import dialogs

title = 'Books'

class BookView(Gtk.Window):
	def __init__(self):
		self.mysql = dbconn.mysql_conn()
		Gtk.Window.__init__(self,title=title)
		self.filtered = False

		#liststores	
		types = Gtk.ListStore(str)
		types.append(['-'])
		types.append(['fiction'])
		types.append(['non-fiction'])
		done = Gtk.ListStore(str)
		done.append(['-'])
		done.append(['True'])
		done.append(['False'])
		self.bookList = Gtk.ListStore(int,str,str,bool,str,str)
		books = self.mysql.getBooks()
		for book in books:
			book = list(book)
			book.append(self.mysql.getTags(book[0]))
			self.bookList.append(book)
		
		#create filter
		self.bookFilter = self.bookList.filter_new()
		self.bookFilter.set_visible_func(self.filter_func)

		#widgets
		self.VLayout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.HLayout = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		self.HLayout2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		self.scrollBars = Gtk.ScrolledWindow()
		self.filterBox = Gtk.Entry()
		self.filterButton = Gtk.Button('Filter')
		self.clearButton = Gtk.Button('Clear')
		self.saveButton = Gtk.Button('Save Changes')
		self.newButton = Gtk.Button('New Book')
		self.deleteButton = Gtk.Button('Delete Book')
		self.titleRadio = Gtk.RadioButton.new_with_label_from_widget(None,'Title')
		self.authorRadio = Gtk.RadioButton.new_with_label_from_widget(self.titleRadio,'Author')
		self.typeCombo = Gtk.ComboBox.new_with_model(types)
		self.doneCombo = Gtk.ComboBox.new_with_model(done)
		self.bookView = Gtk.TreeView.new_with_model(self.bookFilter)

		#renderers
		idRender = Gtk.CellRendererText()
		titleRender = Gtk.CellRendererText()
		authorRender = Gtk.CellRendererText()
		doneRender = Gtk.CellRendererToggle()
		typeRender = Gtk.CellRendererText()
		tagRender = Gtk.CellRendererText()

		#renderer attributes
		titleRender.set_property('editable',True)
		authorRender.set_property('editable',True)
		typeRender.set_property('editable',True)
		tagRender.set_property('editable',True)
		
		#columns
		idCol = Gtk.TreeViewColumn('ID',idRender, text=0)
		titleCol = Gtk.TreeViewColumn('Title',titleRender,text=1)
		authorCol = Gtk.TreeViewColumn('Author',authorRender,text=2)
		doneCol = Gtk.TreeViewColumn('Done',doneRender,active=3)
		typeCol = Gtk.TreeViewColumn('Type',typeRender,text=4)
		tagCol = Gtk.TreeViewColumn('Tags',tagRender,text=5)
	
		#make columns sortable
		idCol.set_sort_column_id(0)
		titleCol.set_sort_column_id(1)
		authorCol.set_sort_column_id(2)
		doneCol.set_sort_column_id(3)

		#add columns to table
		self.bookView.append_column(idCol)
		self.bookView.append_column(titleCol)
		self.bookView.append_column(authorCol)
		self.bookView.append_column(doneCol)
		self.bookView.append_column(typeCol)
		self.bookView.append_column(tagCol)
	
		#create comboboxes
		renderer = Gtk.CellRendererText()
		self.typeCombo.pack_start(renderer,True)
		self.typeCombo.add_attribute(renderer,'text',0)
		self.typeCombo.set_active(0)
		renderer = Gtk.CellRendererText()
		self.doneCombo.pack_start(renderer,True)
		self.doneCombo.add_attribute(renderer,'text',0)
		self.doneCombo.set_active(0)
		
		#connect events
		self.filterButton.connect('clicked',self.filterButtonClicked)
		self.clearButton.connect('clicked',self.clearButtonClicked)
		self.saveButton.connect('clicked',self.saveButtonClicked)
		self.newButton.connect('clicked',self.newButtonClicked)
		self.deleteButton.connect('clicked',self.deleteButtonClicked)
		titleRender.connect('edited',self.titleEdited)
		authorRender.connect('edited',self.authorEdited)
		doneRender.connect('toggled',self.doneEdited)
		typeRender.connect('edited',self.typeEdited)
		tagRender.connect('edited',self.tagsEdited)

		#layout attributes
		self.VLayout.homogenous =False
		self.scrollBars.add(self.bookView)

		#add widgets to layouts 
		self.HLayout.pack_start(self.filterBox,True,True,0)
		self.HLayout.pack_start(self.titleRadio,False,True,0)
		self.HLayout.pack_start(self.authorRadio,False,True,0)
		self.HLayout.pack_start(self.typeCombo,False,True,0)
		self.HLayout.pack_start(self.doneCombo,False,True,0)
		self.HLayout.pack_start(self.filterButton,False,True,0)
		self.HLayout.pack_start(self.clearButton,False,True,0)
		self.HLayout2.pack_start(self.saveButton,True,True,0)
		self.HLayout2.pack_start(self.newButton,True,True,0)
		self.HLayout2.pack_start(self.deleteButton,True,True,0)
		self.VLayout.pack_start(self.scrollBars,True,True,0)
		self.VLayout.pack_start(self.HLayout,False,True,0)
		self.VLayout.pack_start(self.HLayout2,False,True,0)

		#add layouts to window
		self.add(self.VLayout)
		
	def filter_func(self,model,iter,data):
		if not self.filtered:
			return True
		remain = False

		if self.titleRadio.get_active():
			remain = re.search(self.filterBox.get_text(),model[iter][1]) is not None
		elif self.authorRadio.get_active():
			remain = re.search(self.filterBox.get_text(),model[iter][2]) is not None

		if self.filterBox.get_text()=='':
			remain = True

		treeIter = self.typeCombo.get_active_iter()
		if treeIter is not None:
			mode = self.typeCombo.get_model()
			if mode[treeIter][0] != '-':
				remain = remain and (model[iter][4]==mode[treeIter][0])

		treeIter = self.doneCombo.get_active_iter()
		if treeIter is not None:
			mode = self.doneCombo.get_model()
			if mode[treeIter][0] == 'True':	
				remain = remain and model[iter][3]
			elif mode[treeIter][0] == 'False':
				remain = remain and (not model[iter][3])

		return remain

	def filterButtonClicked(self,widget):
		self.filtered=True
		self.bookFilter.refilter()
	
	def clearButtonClicked(self,widget):
		self.filtered=False
		self.bookFilter.refilter()
	
	def saveButtonClicked(self,widget):
		if self.get_title() == title+'*':	
			self.mysql.saveChanges()
			dialog = dialogs.infoDialog(self,'Books Saved', 'Saved Changes')
			self.set_title(title)
			dialog.run()
			dialog.destroy()
	
	def newButtonClicked(self,widget):
		dialog = dialogs.newBookDialog(self)
		done = False
		bookTitle = ''
		author = ''
		done = ''
		typ = ''

		while not done:
			response = dialog.run()
			
			if response == Gtk.ResponseType.CANCEL:
				dialog.destroy()
				return
			
			bookTitle = dialog.titleBox.get_text()
			author = dialog.titleBox.get_text()
			done = dialog.doneCombo.get_active()
			typ = dialog.typeCombo.get_active()
			
			if bookTitle == '' or author == '':
				info = dialogs.infoDialog(self,'Enter Values','Please Fill out all Fields')
				info.run()
				info.destroy()
			else:
				done = True
		
		authorId = self.mysql.getAuthorId(author)
		if authorId is None:
			authorId = self.mysql.insertAuthor(author)
		if done==0:
			done = True
		else:
			done = False

		if typ==0:
			typ = 'fiction'
		else:
			typ = 'non-fiction'

		bookId = self.mysql.insertBook(bookTitle,authorId,done,typ)	
	
		self.bookList.append([bookId,bookTitle,author,done,typ])
		self.set_title(title+'*')
		dialog.destroy()

	def deleteButtonClicked(self,widget):
		selection = self.bookView.get_selection()
		path_index = selection.get_selected_rows()[1][0]
		iterate = self.bookList.get_iter(path_index)
		path_id = selection.get_selected()[1]
		bookId = self.bookFilter.get_value(path_id,0)
	
		self.mysql.deleteBook(bookId)
		self.bookList.remove(iterate)
		self.set_title(title+'*')
  
	def titleEdited(self,widget, path,text):
		self.set_title(title+'*')
		book = self.bookList[path]
		self.mysql.updateTitle(book[0],text)
		book[1]=text

	def authorEdited(self,widget,path,text):
		self.set_title(title+'*')
		book = self.bookList[path]
		authorId = self.mysql.getAuthorId(text)
		if authorId is None:
			authorId = self.mysql.insertAuthor(text)

		self.mysql.updateAuthor(book[0],authorId)

		book[2]=text
			
	def doneEdited(self,widget,path):
		self.set_title(title+'*')	
		book = self.bookList[path]
		self.mysql.updateDone(book[0],not book[3])
		book[3] = not book[3]
	
	def typeEdited(self,widget,path,text):
		if text not in ('fiction','non-fiction'):
			return 
	
		self.set_title(title+'*')
		book = self.bookList[path]	
		self.mysql.updateType(book[0],text)
		book[4] = text
	
	def tagsEdited(self, widget, path, text):
		book = self.bookList[path]
		newTags = text.split(',')
		oldTags = book[5].split(',')

		tagIds = []
		keep = []
		for tag in newTags:	
			if tag != '':
				if tag not in oldTags:
					tagId = self.mysql.getTagId(tag)
					if tagId is None:
						tagId = self.mysql.insertTag(tag)
					tagIds.append(tagId)
				else:
					keep.append(tag)

		for tagId in tagIds:
			self.mysql.tagBook(book[0],tagId)

		for tag in oldTags:
			if tag not in keep and tag!='':
				tagId = self.mysql.getTagId(tag)
				self.mysql.untagBook(book[0],tagId)

		self.set_title(title+"*")
		book[5] = text

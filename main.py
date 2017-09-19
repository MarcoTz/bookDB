import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import dbconn

class BookView(Gtk.Window):
	def __init__(self):
		self.mysql = dbconn.mysql_conn()
		Gtk.Window.__init__(self,title='Books')
		self.VLayout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.VLayout.homogenous =False

		self.scrollBars = Gtk.ScrolledWindow()
		self.bookList = Gtk.ListStore(int,str,str,bool,str)
		books = self.mysql.getBooks()
		for book in books:
			self.bookList.append(list(book))

		
		self.filter = self.bookList.filter_new()
		self.filter.set_visible_func(self.filter_func)
		self.filtered = False

		self.filterBox = Gtk.Entry()
		self.filterButton = Gtk.Button('Filter')
		self.filterButton.connect('clicked',self.filterButtonClicked)
		self.clearButton = Gtk.Button('Clear')
		self.clearButton.connect('clicked',self.clearButtonClicked)
		self.filtered=False;
		self.titleRadio = Gtk.RadioButton.new_with_label_from_widget(None,'Title')
		self.authorRadio = Gtk.RadioButton.new_with_label_from_widget(self.titleRadio,'Author')
		types = Gtk.ListStore(str)
		types.append(['-'])
		types.append(['fiction'])
		types.append(['non-fiction'])
		self.typeCombo = Gtk.ComboBox.new_with_model(types)
		renderer = Gtk.CellRendererText()
		self.typeCombo.pack_start(renderer,True)
		self.typeCombo.add_attribute(renderer,'text',0)
		self.typeCombo.set_active(0)
		done = Gtk.ListStore(str)
		done.append(['-'])
		done.append(['True'])
		done.append(['False'])
		self.doneCombo = Gtk.ComboBox.new_with_model(done)
		renderer = Gtk.CellRendererText()
		self.doneCombo.pack_start(renderer,True)
		self.doneCombo.add_attribute(renderer,'text',0)
		self.doneCombo.set_active(0)

		self.HLayout = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		self.HLayout.pack_start(self.filterBox,True,True,0)
		self.HLayout.pack_start(self.titleRadio,False,True,0)
		self.HLayout.pack_start(self.authorRadio,False,True,0)
		self.HLayout.pack_start(self.typeCombo,False,True,0)
		self.HLayout.pack_start(self.doneCombo,False,True,0)
		self.HLayout.pack_start(self.filterButton,False,True,0)
		self.HLayout.pack_start(self.clearButton,False,True,0)

		self.bookView = Gtk.TreeView.new_with_model(self.filter)
		for i,colTitle in enumerate(['ID','Title','Author','Done','Type']):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(colTitle,renderer,text=i)
			column.set_sort_column_id(i)
			self.bookView.append_column(column)
		
		self.scrollBars.add(self.bookView)
		self.VLayout.pack_start(self.scrollBars,True,True,0)
		self.VLayout.pack_start(self.HLayout,False,True,0)
		self.add(self.VLayout)

	def filter_func(self,model,iter,data):
		if not self.filtered:
			return True
		remain = False

		if self.titleRadio.get_active():
			remain = model[iter][1] == self.filterBox.get_text()
		elif self.authorRadio.get_active():
			remain = model[iter][2] == self.filterBox.get_text()

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
		self.filter.refilter()
	
	def clearButtonClicked(self,widget):
		self.filtered=False
		self.filter.refilter()


win = BookView()
win.connect('delete-event',Gtk.main_quit)
win.title='test'
win.show_all()
Gtk.main()

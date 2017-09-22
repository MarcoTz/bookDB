import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

class infoDialog(Gtk.Dialog):
	
	def __init__(self,parent,title,info):
		Gtk.Dialog.__init__(self,title,parent,0,
			(Gtk.STOCK_OK, Gtk.ResponseType.OK))

		label = Gtk.Label(info)
		box = self.get_content_area()
		box.add(label)
		self.show_all()

class newBookDialog(Gtk.Dialog):
	
	def __init__(self,parent):
		Gtk.Dialog.__init__(self,'New Book',parent,0,
			(Gtk.STOCK_OK, Gtk.ResponseType.OK,
			Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

		titleLabel = Gtk.Label('Title: ')
		self.titleBox = Gtk.Entry()
		authorLabel = Gtk.Label('Author: ')
		self.authorBox = Gtk.Entry()
		doneLabel = Gtk.Label('Done: ')

		doneList = Gtk.ListStore(bool)
		doneList.append([True])
		doneList.append([False])
		self.doneCombo = Gtk.ComboBox.new_with_model(doneList)
		renderer = Gtk.CellRendererText()
		self.doneCombo.pack_start(renderer,True)
		self.doneCombo.add_attribute(renderer,'text',0)
		self.doneCombo.set_active(0)
		
		typeLabel = Gtk.Label('Type: ')

		typeList = Gtk.ListStore(str)
		typeList.append(['fiction'])
		typeList.append(['non-fiction'])
		self.typeCombo = Gtk.ComboBox.new_with_model(typeList)
		renderer = Gtk.CellRendererText()
		self.typeCombo.pack_start(renderer,True)
		self.typeCombo.add_attribute(renderer,'text',0)
		self.typeCombo.set_active(0)

		tagLabel = Gtk.Label('Tags(Comma separated): ')
		self.tagBox = Gtk.Entry()

		box = self.get_content_area()
		box.add(titleLabel)
		box.add(self.titleBox)
		box.add(authorLabel)
		box.add(self.authorBox)
		box.add(doneLabel)
		box.add(self.doneCombo)
		box.add(typeLabel)
		box.add(self.typeCombo)
		box.add(tagLabel)
		box.add(self.tagBox)

		self.show_all()

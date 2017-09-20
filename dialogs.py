import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

class saveInfo(Gtk.Dialog):
	
	def __init__(self,parent):
		Gtk.Dialog.__init__(self,'Saved Books',parent,0,
			(Gtk.STOCK_OK, Gtk.ResponseType.OK))

		label = Gtk.Label('Saved Changes')
		box = self.get_content_area()
		box.add(label)
		self.show_all()

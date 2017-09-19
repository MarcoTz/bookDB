import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import bookview


win = bookview.BookView()
win.connect('delete-event',Gtk.main_quit)
win.title='test'
win.show_all()
Gtk.main()

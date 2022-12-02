import json
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio

(TARGET_ENTRY_TEXT, TARGET_ENTRY_PIXBUF) = range(2)
(COLUMN_TEXT, COLUMN_PIXBUF) = range(2)

f = open("commands.json")
command = json.load(f)

a = open("amode238.txt")
amode = json.load(a)

commands = []
autos = []

for i in command:
    commands.append((i["Command"][0]["Name"], i["Command"][1]["params"][0]))
print(commands)
for i in amode["AutonomousModes"]:
    autos.append((i["Name"]))
class DragDropWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Drag and Drop Demo")
        self.set_border_width(10)
        
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid) 

        self.amodeListBox = Gtk.ListBox()
        self.builderListBox = Gtk.ListBox()
        self.commandListBox = Gtk.ListBox()
        for i in commands:
            self.commandListBox.add(Gtk.Label(i[0]))
        self.commandListBox.add(Gtk.Label("Commands"))
        for i in autos:
            self.amodeListBox.add(Gtk.Label(i))
            
        self.grid.attach(self.amodeListBox, 0, 0, 8, 10)
        self.grid.attach(self.builderListBox, 8, 0, 8, 10)
        self.grid.attach(self.commandListBox, 16, 0, 8, 10)
        
        def on_selection_button_clicked(self, widget):
            print("clicked")
        
        

        self.show_all()


win = DragDropWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

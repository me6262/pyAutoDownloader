import json
import gi

# TODO: add comments everywhere
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio

(TARGET_ENTRY_TEXT, TARGET_ENTRY_PIXBUF) = range(2)
(COLUMN_TEXT, COLUMN_PIXBUF) = range(2)

f = open("commands.json")
command = json.load(f)

a = open("amode238.txt")
amode = json.load(a)

current_mode = []
commands = []
autos = []
selected_auto = 0
selected_command = 0
for i in command:
    commands.append((i["Command"][0]["Name"], i["Command"][1]["params"][0]))
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

        def on_amode_selected(obj, widget):
            print("clicked")
            print(obj.get_selected_rows()[0].get_children()[0].get_text())
            mode_location = obj.get_selected_rows()[0].get_index()

            selected_auto = mode_location
            mode_name = obj.get_selected_rows()[0].get_children()[0].get_text()
            #print(amode["AutonomousModes"][mode_location])
            for row in self.builderListBox.get_children():
                row.destroy()
            for i in amode["AutonomousModes"][mode_location]["Commands"]:
                row = Gtk.ListBoxRow()
                label = Gtk.Label()
                label.set_text(i["Name"])
                row.add(label)
                self.builderListBox.add(row)
                print(i["Name"])
                self.show_all()
        def on_amode_command_selected(obj, widget):
            print("clicked")
            command_location = obj.get_selected_rows()[0].get_index()
            selected_command = command_location
            command_name = obj.get_selected_rows()[0].get_children()[0].get_text()
            #print(amode["AutonomousModes"][mode_location])
            for row in self.paramsListBox.get_children():
                row.destroy()
            try:
                params = amode["AutonomousModes"][selected_auto]["Commands"][command_location]["Parameters"]

            except:
                params = []
            if params != []:
                for i in params:
                    row = Gtk.ListBoxRow()
                    entry = Gtk.Entry()
                    entry.set_text(i) 
                    row.add(entry)
                    self.paramsListBox.add(row)
            row = Gtk.ListBoxRow()
            combo = Gtk.ComboBoxText()
            parallel_mode = amode["AutonomousModes"][selected_auto]["Commands"][command_location]["ParallelType"]

            combo.append_text("Parallel")
            combo.append_text("Race")
            combo.append_text("Deadline_Leader")
            combo.append_text("Deadline_Follower")
            combo.append_text("None")
            if parallel_mode != "None":
                if parallel_mode == "Parallel":
                    combo.set_active(0)
                elif parallel_mode == "Race":
                    combo.set_active(1)
                elif parallel_mode == "Deadline_Leader":
                    combo.set_active(2)
                elif parallel_mode == "Deadline_Follower":
                    combo.set_active(3)
            else:
                combo.set_active(4)

            row.add(combo)
            self.paramsListBox.add(row)
            self.show_all()
            



        self.amodeFrame = Gtk.Frame(label="Autonomous Modes")
        self.commandFrame = Gtk.Frame(label="Commands")
        self.builderFrame = Gtk.Frame(label="Auto Editor")
        self.paramsFrame = Gtk.Frame(label="Parameters")
        self.amodeListBox = Gtk.ListBox()
        self.builderListBox = Gtk.ListBox()
        self.paramsListBox = Gtk.ListBox()
        self.commandListBox = Gtk.ListBox()
        for i in commands:
            self.commandListBox.add(Gtk.Label(i[0]))
        self.commandListBox.add(Gtk.Label("Commands"))
        for i in autos:
            row = Gtk.ListBoxRow()
            label = Gtk.Label()
            label.set_text(i)
            row.add(label)
            self.amodeListBox.add(row)
            
        self.amodeFrame.add(self.amodeListBox)
        self.commandFrame.add(self.commandListBox)
        self.builderFrame.add(self.builderListBox)
        self.paramsFrame.add(self.paramsListBox)

            
        self.amodeListBox.connect("row-selected", on_amode_selected)
        self.builderListBox.connect("row-selected", on_amode_command_selected)
        # self.grid.attach(self.amodeListBox, 0, 0, 8, 10)
        self.grid.set_column_spacing(10)
        self.grid.attach(self.amodeFrame, 8, 0, 8, 10)
        self.grid.attach(self.builderFrame, 16, 0, 8, 5)
        self.grid.attach(self.paramsFrame, 16, 5, 8, 5)
        self.grid.attach(self.commandFrame, 24, 0, 8, 10)
        
        
        


        self.show_all()


win = DragDropWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

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
selected_command = 0
for i in command:
    commands.append((i["Command"][0]["Name"], i["Command"][1]["params"][0]))
for i in amode["AutonomousModes"]:
    autos.append((i["Name"]))
class DragDropWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Autonomous Mode Builder")
        self.selected_auto = 0
        self.set_border_width(10)
        
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid) 

        #when the autonmous mode is selected from the list on the right
        def on_amode_selected(obj, widget):
            for row in self.paramsListBox:
                self.paramsListBox.remove(row)
            print("clicked")
            print(obj.get_selected_rows()[0].get_children()[0].get_text())
            mode_location = obj.get_selected_rows()[0].get_index()

            current_mode = amode["AutonomousModes"][mode_location]
            self.selected_auto = mode_location
            mode_name = obj.get_selected_rows()[0].get_children()[0].get_text()
            # kill all of the previous commands in the builder ListBox
            for row in self.builderListBox.get_children():
                row.destroy()
            # add the commands to the builder listbox
            for i in amode["AutonomousModes"][mode_location]["Commands"]:
                row = Gtk.ListBoxRow()
                label = Gtk.Label()
                label.set_text(i["Name"])
                row.add(label)
                self.builderListBox.add(row)
                self.show_all()
        # when a command is selected from the Builder listbox we add all of the parameters
        # of that command to the parameters listbox
        def on_amode_command_selected(obj, widget):
            print("clicked")
            command_location = obj.get_selected_rows()[0].get_index()
            #print(amode["AutonomousModes"][mode_location])
            for row in self.paramsListBox.get_children():
                row.destroy()
            try:
                params = amode["AutonomousModes"][self.selected_auto]["Commands"][command_location]["Parameters"]

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
            parallel_mode = amode["AutonomousModes"][self.selected_auto]["Commands"][command_location]["ParallelType"]

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
        
        self.add_command_button = Gtk.Button(label="<-")
        self.command_up_button = Gtk.Button(label="^")
        self.command_down_button = Gtk.Button(label="v")

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

        
        self.grid.set_column_spacing(10)
        self.grid.attach(self.amodeFrame, 4, 0, 4, 24)
        self.grid.attach(self.builderFrame, 8, 0, 4, 12)
        self.grid.attach(self.paramsFrame, 8, 12, 4, 12)
        self.grid.attach(self.add_command_button, 12, 1, 1, 1)
        self.grid.attach(self.command_up_button, 12, 2, 1, 1)
        self.grid.attach(self.command_down_button, 12, 3, 1, 1)
        self.grid.attach(self.commandFrame, 13, 0, 4, 24)
        

        self.show_all()


win = DragDropWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

import commands238
import json
import gi


# TODO: add comments everywhere
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio

(TARGET_ENTRY_TEXT, TARGET_ENTRY_PIXBUF) = range(2)
(COLUMN_TEXT, COLUMN_PIXBUF) = range(2)


com238 = commands238


prevpath = open("prevFilepath.txt")
path = prevpath.readlines()[-1]
a = open(path + "/src/main/deploy/amode238.txt")
print(prevpath.read())
command = com238.get_commands(path)
print(path + "/src/main/deploy/amode238.txt")
amode = json.load(a)

current_mode = []
commands = []
selected_command = 0
# for i in command:
    # commands.append((i["Command"][0]["Name"], i["Command"][1]["params"][0]))
class amodeWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Autonomous Mode Builder")
        self.selected_auto = 0
        self.set_border_width(10)
        
        # self.add(bar)
        
        self.autos = []
        for i in amode["AutonomousModes"]:
            self.autos.append((i["Name"]))
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid) 

        self.saveButton = Gtk.Button(label="Save")
        self.loadButton = Gtk.Button(label="Load")
        self.saveButton.connect("clicked", self.on_save_clicked)
        self.other_button = Gtk.Button(label="Json View")
        #when the autonmous mode is selected from the list on the right
        
        self.loadButton.connect("clicked", self.on_load_clicked)
        
        self.headerBar = Gtk.HeaderBar()
        self.headerBar.set_show_close_button(True)
        self.headerBar.props.title = "Autonomous Mode Builder"
        self.headerBar.pack_start(self.saveButton) 
        self.headerBar.pack_start(self.loadButton)    
        self.headerBar.pack_end(self.other_button)
        self.other_button.connect("clicked", self.on_json_clicked)
        self.set_titlebar(self.headerBar)
        
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
        self.remove_command_button = Gtk.Button(label="--")
        
        self.add_amode_button = Gtk.Button(label="+")
        self.rename_amode_button = Gtk.Button(label="*")
        
        self.amodeFrame.add(self.amodeListBox)
        self.commandFrame.add(self.commandListBox)
        self.builderFrame.add(self.builderListBox)
        self.paramsFrame.add(self.paramsListBox)

        self.add_command_button.connect("clicked", self.on_add_command_clicked)
        self.command_down_button.connect("clicked", self.on_command_down_clicked)
        self.command_up_button.connect("clicked", self.on_command_up_clicked)
        self.remove_command_button.connect("clicked", self.on_remove_command_clicked)
        self.rename_amode_button.connect("clicked", self.on_rename_amode)
            
        self.amodeListBox.connect("row-selected", self.on_amode_selected)
        self.commandListBox.connect("drag-begin", self.on_command_drag_begin)
        self.builderListBox.connect("row-selected", self.on_amode_command_selected)
        self.builderListBox.connect("drag-data-received", self.on_amode_command_drag_end)
        self.add_amode_button.connect("clicked", self.on_add_amode_clicked)
        # self.other_button.connect("clicked", self.on_other_clicked)

        
        self.grid.set_column_spacing(10)
        self.grid.attach(self.saveButton, 0, 0, 2, 1)
        self.grid.attach(self.loadButton, 2, 0, 2, 1)
        self.grid.attach(self.add_amode_button, 4, 2, 1, 1)
        self.grid.attach(self.rename_amode_button, 4, 3, 1, 1)
        self.grid.attach(self.amodeFrame, 0, 1, 4, 20)
        self.grid.attach(self.builderFrame, 5, 1, 4, 10)
        self.grid.attach(self.paramsFrame, 5, 11, 4, 10)
        self.grid.attach(self.add_command_button, 9, 2, 1, 1)
        self.grid.attach(self.command_up_button, 9, 3, 1, 1)
        self.grid.attach(self.command_down_button, 9, 4, 1, 1)
        self.grid.attach(self.remove_command_button, 9, 5, 1, 1)
        self.grid.attach(self.commandFrame, 10, 1, 4, 20)
        

        self.show_all()

    def build_list(self):
        if self.amodeListBox.get_children():
            for row in self.amodeListBox:
                self.amodeListBox.remove(row)
        if self.commandListBox.get_children():
            for row in self.commandListBox:
                self.commandListBox.remove(row)
        for i in amode["AutonomousModes"]:
            row = Gtk.ListBoxRow()
            row.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [], Gdk.DragAction.COPY)
            label = Gtk.Label()
            label.set_text(i["Name"])
            row.add(label)
            self.amodeListBox.add(row)

        for i in command:
            commands.append((i["Command"][0]["Name"], i["Command"][1]["params"][0]))
        for i in commands:
            print(i)
            self.commandListBox.add(Gtk.Label(i[0]))
        self.trajectories = com238.get_trajectories(path)
        
        
        self.show_all()
    
    def on_amode_selected(self, widget, obj):
        for row in self.paramsListBox:
            self.paramsListBox.remove(row)
        print("clicked")
        print(obj.get_parent().get_selected_rows()[0].get_children()[0].get_text())
        mode_location = obj.get_parent().get_selected_rows()[0].get_index()

        self.current_mode = amode["AutonomousModes"][mode_location]
        self.selected_auto = mode_location
        mode_name = obj.get_parent().get_selected_rows()[0].get_children()[0].get_text()
        # kill all of the previous commands in the builder ListBox
        for row in self.builderListBox.get_children():
            row.destroy()
        # add the commands to the builder listbox
        for i in amode["AutonomousModes"][mode_location]["Commands"]:
            row = Gtk.ListBoxRow()
            label = Gtk.Label()
            label.set_text(i["Name"])
            row.add(label)
            row.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [], Gdk.DragAction.COPY)
            row.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
            # row.connect('activate', self.on_rename_amode)
            self.builderListBox.add(row)
            self.show_all()
    # when a command is selected from the Builder listbox we add all of the parameters
    # of that command to the parameters listbox
    def on_amode_command_selected(self, widget, obj):
        print("clicked")
        self.command_location = obj.get_parent().get_selected_rows()[0].get_index()
        #print(amode["AutonomousModes"][mode_location])
        for row in self.paramsListBox.get_children():
            row.destroy()
        try:
            params = amode["AutonomousModes"][self.selected_auto]["Commands"][self.command_location]["Parameters"]

        except:
            params = []
        if params != []:
            for i in params:
                if amode["AutonomousModes"][self.selected_auto]["Commands"][self.command_location]["Name"] == "TrajectoryDriveCommand": 
                    row = Gtk.ListBoxRow()
                    combobox = Gtk.ComboBoxText()
                    for j in range(len(self.trajectories)):
                        combobox.append_text(self.trajectories[j])
                        if i == self.trajectories[j]:
                            combobox.set_active(j)
                    combobox.connect("changed", self.on_command_changed)
                    combobox.set_title("Trajectory")
                    row.add(combobox)
                    self.paramsListBox.add(row)
                else:        
                    row = Gtk.ListBoxRow()
                    entry = Gtk.Entry()
                    entry.set_text(i)
                    entry.connect("changed", self.on_command_changed) 
                    row.add(entry)
                    self.paramsListBox.add(row)

                
        row = Gtk.ListBoxRow()
        combo = Gtk.ComboBoxText()
        parallel_mode = amode["AutonomousModes"][self.selected_auto]["Commands"][self.command_location]["ParallelType"]

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

        combo.connect("changed", self.on_command_changed)
        row.add(combo)
        self.paramsListBox.add(row)
        self.show_all()

    def on_command_changed(self, obj):
        if (type(obj) == Gtk.ComboBoxText and obj.get_title() != "Trajectory"):
            amode["AutonomousModes"][self.selected_auto]["Commands"][self.command_location]["ParallelType"] = obj.get_active_text()
        else:
            if (obj.get_title() == "Trajectory"):
                amode["AutonomousModes"][self.selected_auto]["Commands"][self.command_location]["Parameters"][obj.get_parent().get_index()] = obj.get_active_text()
            else:
                amode["AutonomousModes"][self.selected_auto]["Commands"][self.command_location]["Parameters"][obj.get_parent().get_index()] = obj.get_text()
        print(amode["AutonomousModes"][self.selected_auto]["Commands"])
        # print(obj.get_active_text())
        print("changed")
        
    def on_save_clicked(self, widget):
        print("save")
        with open(path + "src/main/deploy/amode238.json", "w") as f:
            json.dump(amode, f, indent=4)
    
    # creates a new file chooser dialog and the selected file is loaded as json
    def on_load_clicked(self, widget):
        print("load")
        dialog = Gtk.FileChooserDialog("Please choose a file", self, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog.set_current_folder(path)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())

            with open(dialog.get_current_folder() + '/src/main/deploy/amode238.txt', "r") as f:
                global amode
                amode = json.load(f)
                open('prevFilepath.txt', 'w').write(dialog.get_current_folder())
                self.build_list()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
        dialog.destroy()
        

    def on_add_command_clicked(self, widget):
        print("add command")
        print(self.commandListBox.get_selected_rows()[0].get_children()[0].get_text())
        if command[self.commandListBox.get_selected_rows()[0].get_index()]["Command"][1]["params"] != [""]:
            amode["AutonomousModes"][self.selected_auto]["Commands"].append({"Name": self.commandListBox.get_selected_rows()[0].get_children()[0].get_text(), "Parameters": command[self.commandListBox.get_selected_rows()[0].get_index()]["Command"][1]["params"], "ParallelType": "None"})
        else: 
            amode["AutonomousModes"][self.selected_auto]["Commands"].append({"Name": self.commandListBox.get_selected_rows()[0].get_children()[0].get_text(), "Parameters": [], "ParallelType": "None"})
        row = Gtk.ListBoxRow()
        row.add(Gtk.Label(self.commandListBox.get_selected_rows()[0].get_children()[0].get_text()))
        self.builderListBox.add(row)
        print(amode["AutonomousModes"][self.selected_auto]["Commands"])
        self.show_all()
    
    def on_command_up_clicked(self, widget):
        print("up")
        if self.command_location > 0:
            temp = amode["AutonomousModes"][self.selected_auto]["Commands"][self.command_location]
            amode["AutonomousModes"][self.selected_auto]["Commands"][self.command_location] = amode["AutonomousModes"][self.selected_auto]["Commands"][self.command_location - 1]
            amode["AutonomousModes"][self.selected_auto]["Commands"][self.command_location - 1] = temp
            self.command_location -= 1
            for row in self.builderListBox.get_children():
                row.destroy()
            for i in amode["AutonomousModes"][self.selected_auto]["Commands"]:
                row = Gtk.ListBoxRow()
                label = Gtk.Label()
                label.set_text(i["Name"])
                row.add(label)
                self.builderListBox.add(row)
                self.show_all()
            self.builderListBox.select_row(self.builderListBox.get_row_at_index(self.command_location))
            self.on_amode_command_selected(self, self.builderListBox)
        
    def on_command_down_clicked(self, widget):
        print("down")
        if self.command_location < len(amode["AutonomousModes"][self.selected_auto]["Commands"]) - 1:
            temp = amode["AutonomousModes"][self.selected_auto]["Commands"][self.command_location]
            amode["AutonomousModes"][self.selected_auto]["Commands"][self.command_location] = amode["AutonomousModes"][self.selected_auto]["Commands"][self.command_location + 1]
            amode["AutonomousModes"][self.selected_auto]["Commands"][self.command_location + 1] = temp
            self.command_location += 1
            for row in self.builderListBox.get_children():
                row.destroy()
            for i in amode["AutonomousModes"][self.selected_auto]["Commands"]:
                row = Gtk.ListBoxRow()
                label = Gtk.Label()
                label.set_text(i["Name"])
                row.add(label)
                self.builderListBox.add(row)
                self.show_all()
            self.builderListBox.select_row(self.builderListBox.get_row_at_index(self.command_location))
            self.on_amode_command_selected(self, widget, obj=self.builderListBox.get_selected_rows()[0])
    
    def on_remove_command_clicked(self, widget):
        print("remove")
        amode["AutonomousModes"][self.selected_auto]["Commands"].pop(self.command_location)
        for row in self.builderListBox.get_children():
            row.destroy()
        for i in amode["AutonomousModes"][self.selected_auto]["Commands"]:
            row = Gtk.ListBoxRow()
            label = Gtk.Label()
            label.set_text(i["Name"])
            row.add(label)
            self.builderListBox.add(row)
            self.show_all()
        if self.command_location > 0:
            self.command_location -= 1
            self.builderListBox.select_row(self.builderListBox.get_row_at_index(self.command_location))
            self.on_amode_command_selected(self, self.builderListBox)
        else:
            self.paramsListBox.foreach(lambda x: x.destroy())
            self.show_all()
    
    #TODO: make drag and drop work
    def on_amode_command_drag_end(self, widget, context, x, y, time):
        print("drag")
        self.command_location = self.builderListBox.get_row_at_y(y).get_index()
        row = Gtk.ListBoxRow()
        row.add(Gtk.Label(command[self.command_location]["Command"][0]))
        print(self.command_location)
        self.show_all()

    #TODO: make drag and drop work    
    def on_command_drag_begin(self, widget, context):
        print("drag begin")
        self.command_location = self.commandListBox.get_selected_rows()[0].get_index()
        row = Gtk.ListBoxRow()
        row.add(Gtk.Label(command[self.command_location]["Command"][0]))
        self.show_all()
        
    def on_add_amode_clicked(self, widget):
        print("add amode")
        amode["AutonomousModes"].append({"Name": "New Mode", "Commands": []})
        row = Gtk.ListBoxRow()
        row.add(Gtk.Label("New Mode"))
        self.amodeListBox.add(row)
        self.selected_auto = len(amode["AutonomousModes"]) - 1
        self.show_all()
        
    def on_rename_amode(self, widget):
        print("rename amode")
        dialog = Gtk.Dialog()
        
        entry = Gtk.Entry()
        name = self.amodeListBox.get_selected_rows()[0].get_child().get_text()
        entry.set_text(name)
        # dialog.get_child().add(entry)
        dialog.add_button("Ok", Gtk.ResponseType.OK)
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.get_content_area().add(entry)
        dialog.show_all()
        response = dialog.run()
        
        self.show_all()
        print(name)
        if response == Gtk.ResponseType.OK:
            print("did a thing")
            amode["AutonomousModes"][self.selected_auto]["Name"] = entry.get_text()
            self.amodeListBox.get_selected_rows()[0].get_child().set_text(entry.get_text())
            self.show_all()
        else:
            pass
        dialog.destroy()
    
    def on_json_clicked(self, widget):
        print("other")
        # this will make a dialog showing a preview of the generated json
        dialog = Gtk.Dialog()
        dialog.add_button("Cool", Gtk.ResponseType.OK)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_min_content_height(500)
        scrolled.set_min_content_width(400)
        scrolled.add(Gtk.Label(json.dumps(amode, indent=2)))
        dialog.get_content_area().add(scrolled)
        dialog.show_all()
        response = dialog.run()
        if (response == Gtk.ResponseType.OK):
            dialog.destroy()
        
    
win = amodeWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

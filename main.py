# -------------------------------------#
# Program: Autonomous Mode Builder
# authors: Hayden Mitchell
# -------------------------------------#

import commands238
import json
import gi
import os

# TODO: add comments everywhere
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio

(TARGET_ENTRY_TEXT, TARGET_ENTRY_PIXBUF) = range(2)
(COLUMN_TEXT, COLUMN_PIXBUF) = range(2)

DRAG_ACTION = Gdk.DragAction.COPY

com238 = commands238
txtPath = '/src/main/deploy/amode238.txt'
txtNTPath = '\\src\\main\\deploy\\amode238.txt'

if os.name == "posix":
    prevpath = open('prevFilepath.txt')
    path = prevpath.readlines()[-1]
    fullpath = path + txtPath
else:
    prevpath = open('prevNTpath.txt')
    path = prevpath.readlines()[-1]
    fullpath = path + txtNTPath
current_mode = []
commands = []
selected_command = 0


class amodeWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title="Autonomous Mode Builder")
        self.selected_auto = 0
        self.command = []
        self.set_border_width(10)

        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        # icons for buttons to be used later
        openico = Gtk.Image.new_from_icon_name("document-open-symbolic",
                                               Gtk.IconSize.BUTTON)
        saveico = Gtk.Image.new_from_icon_name("document-save",
                                               Gtk.IconSize.BUTTON)
        burgerico = Gtk.Image.new_from_icon_name("hamburger-menu",
                                                 Gtk.IconSize.BUTTON)
        newico = Gtk.Image.new_from_icon_name("document-new",
                                              Gtk.IconSize.BUTTON)
        removeico = Gtk.Image.new_from_icon_name("edit-delete",
                                                 Gtk.IconSize.BUTTON)
        upico = Gtk.Image.new_from_icon_name("go-up", Gtk.IconSize.BUTTON)
        downico = Gtk.Image.new_from_icon_name("go-down", Gtk.IconSize.BUTTON)
        renameico = Gtk.Image.new_from_icon_name("edit-rename",
                                                 Gtk.IconSize.BUTTON)
        addico = Gtk.Image.new_from_icon_name("add", Gtk.IconSize.BUTTON)

        self.saveButton = Gtk.Button(image=saveico)
        self.loadButton = Gtk.Button(image=openico)
        self.saveButton.connect("clicked", self.on_save_clicked)
        self.other_button = Gtk.MenuButton(image=burgerico)
        self.json_button = Gtk.Button(label="JSON preview")
        self.about_button = Gtk.Button(label='About')
        #when the autonmous mode is selected from the list on the right

        self.other_popover = Gtk.Popover()
        self.other_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                                  spacing=6)
        self.other_vbox.add(self.json_button)
        self.other_vbox.add(self.about_button)

        self.other_vbox.show_all()
        self.other_popover.add(self.other_vbox)
        self.other_popover.set_position(Gtk.PositionType.BOTTOM)
        self.other_button.set_popover(self.other_popover)
        self.loadButton.connect("clicked", self.on_load_clicked)

        self.headerBar = Gtk.HeaderBar()
        self.headerBar.set_show_close_button(True)
        self.headerBar.props.title = "Autonomous Mode Builder"
        self.headerBar.pack_start(self.saveButton)
        self.headerBar.pack_start(self.loadButton)
        self.headerBar.pack_end(self.other_button)
        self.set_titlebar(self.headerBar)

        self.amodeFrame = Gtk.Frame(label="Autonomous Modes")
        self.commandFrame = Gtk.Frame(label="Commands")
        self.builderFrame = Gtk.Frame(label="Auto Editor")
        self.paramsFrame = Gtk.Frame(label="Parameters")

        self.amodeListBox = Gtk.ListBox()
        self.builderListBox = Gtk.ListBox()
        self.paramsListBox = Gtk.ListBox()
        self.commandListBox = Gtk.ListBox()

        self.add_command_button = Gtk.Button(image=addico)
        self.command_up_button = Gtk.Button(image=upico)
        self.command_down_button = Gtk.Button(image=downico)
        self.remove_command_button = Gtk.Button(image=removeico)

        self.add_amode_button = Gtk.Button(image=newico)
        self.rename_amode_button = Gtk.Button(image=renameico)

        self.amodeFrame.add(self.amodeListBox)
        self.commandFrame.add(self.commandListBox)
        self.builderFrame.add(self.builderListBox)
        self.paramsFrame.add(self.paramsListBox)

        self.add_command_button.connect("clicked", self.on_add_command_clicked)
        self.command_down_button.connect("clicked",
                                         self.on_command_down_clicked)
        self.command_up_button.connect("clicked", self.on_command_up_clicked)
        self.remove_command_button.connect("clicked",
                                           self.on_remove_command_clicked)
        self.rename_amode_button.connect("clicked", self.on_rename_amode)
        self.json_button.connect("clicked", self.on_json_clicked)
        self.about_button.connect("clicked", self.aboutPage)

        self.amodeListBox.connect("row-selected", self.on_amode_selected)
        self.builderListBox.connect("row-selected",
                                    self.on_amode_command_selected)
        self.add_amode_button.connect("clicked", self.on_add_amode_clicked)

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
        self.command = com238.get_commands(path)
        print('printing command')
        print(self.command)
        if self.amodeListBox.get_children():
            for row in self.amodeListBox:
                self.amodeListBox.remove(row)
        if self.commandListBox.get_children():
            for row in self.commandListBox:
                self.commandListBox.remove(row)
        for i in self.amode["AutonomousModes"]:
            row = Gtk.ListBoxRow()
            row.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [],
                                Gdk.DragAction.COPY)
            label = Gtk.Label()
            label.set_text(i["Name"])
            row.add(label)
            self.amodeListBox.add(row)

        for i in self.command:
            commands.append(
                (i["Command"][0]["Name"], i["Command"][1]["params"][0]))
        for i in commands:
            self.commandListBox.add(Gtk.Label(i[0]))
        self.trajectories = com238.get_trajectories(path)

        self.show_all()

    def on_amode_selected(self, widget, obj):
        for row in self.paramsListBox:
            self.paramsListBox.remove(row)
        print("clicked")
        print(obj.get_parent().get_selected_rows()[0].get_children()
              [0].get_text())
        mode_location = obj.get_parent().get_selected_rows()[0].get_index()

        self.current_mode = self.amode["AutonomousModes"][mode_location]
        self.selected_auto = mode_location
        mode_name = obj.get_parent().get_selected_rows()[0].get_children(
        )[0].get_text()
        # kill all of the previous commands in the builder ListBox
        for row in self.builderListBox.get_children():
            row.destroy()
        # add the commands to the builder listbox
        for i in self.amode["AutonomousModes"][mode_location]["Commands"]:
            row = Gtk.ListBoxRow()
            label = Gtk.Label()
            label.set_text(i["Name"])
            row.add(label)
            row.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [],
                                Gdk.DragAction.COPY)
            row.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
            # row.connect('activate', self.on_rename_amode)
            self.builderListBox.add(row)
            self.show_all()

    # when a command is selected from the Builder listbox we add all of the parameters
    # of that command to the parameters listbox
    def on_amode_command_selected(self, widget, obj):
        print("clicked")
        self.command_location = obj.get_parent().get_selected_rows(
        )[0].get_index()
        for row in self.paramsListBox.get_children():
            row.destroy()
        try:
            params = self.amode["AutonomousModes"][self.selected_auto][
                "Commands"][self.command_location]["Parameters"]

        except:
            params = []
        if params != []:
            for i in params:
                if self.amode["AutonomousModes"][
                        self.selected_auto]["Commands"][self.command_location][
                            "Name"] == "TrajectoryDriveCommand":
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
        parallel_mode = self.amode["AutonomousModes"][self.selected_auto][
            "Commands"][self.command_location]["ParallelType"]

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
            self.amode["AutonomousModes"][self.selected_auto]["Commands"][
                self.command_location]["ParallelType"] = obj.get_active_text()
        else:
            try:
                if (obj.get_title() == "Trajectory"):
                    self.amode["AutonomousModes"][self.selected_auto][
                        "Commands"][self.command_location]["Parameters"][
                            obj.get_parent().get_index(
                            )] = obj.get_active_text()
                else:
                    self.amode["AutonomousModes"][self.selected_auto][
                        "Commands"][self.command_location]["Parameters"][
                            obj.get_parent().get_index()] = obj.get_text()
            except:
                self.amode["AutonomousModes"][self.selected_auto]["Commands"][
                    self.command_location]["Parameters"][
                        obj.get_parent().get_index()] = obj.get_text()
        print(self.amode["AutonomousModes"][self.selected_auto]["Commands"])
        # print(obj.get_active_text())
        print("changed")

    def on_save_clicked(self, widget):
        print("save")
        if os.name == 'posix':
            with open(path + txtPath, "w") as f:
                json.dump(self.amode, f, indent=4)
        else:
            with open(path + txtNTPath, "w") as f:
                json.dump(self.amode, f, indent=4)

    # creates a new file chooser dialog and the selected file is loaded as json
    def on_load_clicked(self, widget):
        errorDialog = Gtk.MessageDialog()
        errorDialog.set_title("what'd you break now?")
        print("load")
        dialog = Gtk.FileChooserDialog(
            "Please choose a file", self, Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN,
             Gtk.ResponseType.OK))
        dialog.set_current_folder(path)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
            try:
                if os.name == "nt":
                    with open(dialog.get_current_folder() + txtNTPath, "r") as f:
                        print('here')
                        self.amode = json.load(f)
                        open('prevNTpath.txt',
                            'w').write(dialog.get_current_folder())
                    print(dialog.get_current_folder())
                    self.build_list()

                else:
                    with open(dialog.get_current_folder() + txtPath, "r") as f:
                        self.amode = json.load(f)
                        open('prevFilepath.txt',
                            'w').write(dialog.get_current_folder())
                    self.build_list()
            except:
                print(dialog.get_current_folder() + txtNTPath)
                dialog.destroy()
                errorDialog.add_button("OK", Gtk.ResponseType.OK)
                errorDialog.set_markup("Please pick a valid project folder's root directory")
                errorDialog.format_secondary_text("")
                response2 = errorDialog.run()
                if response2 == Gtk.ResponseType.OK:
                    print("cool")
                    errorDialog.destroy()
                
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
        dialog.destroy()

    def on_add_command_clicked(self, widget):
        print("add command")
        print(self.commandListBox.get_selected_rows()[0].get_children()
              [0].get_text())
        print(self.command)
        if self.command[self.commandListBox.get_selected_row().get_index(
        )]["Command"][1]["params"] != ['']:
            self.amode["AutonomousModes"][
                self.selected_auto]["Commands"].append({
                    "Name":
                    self.commandListBox.get_selected_rows()[0].get_children()
                    [0].get_text(),
                    "Parameters":
                    self.command[self.commandListBox.get_selected_rows()
                                 [0].get_index()]["Command"][1]["params"],
                    "ParallelType":
                    "None"
                })
        else:
            self.amode["AutonomousModes"][
                self.selected_auto]["Commands"].append({
                    "Name":
                    self.commandListBox.get_selected_rows()[0].get_children()
                    [0].get_text(),
                    "Parameters": [],
                    "ParallelType":
                    "None"
                })
        row = Gtk.ListBoxRow()
        row.add(
            Gtk.Label(self.commandListBox.get_selected_rows()
                      [0].get_children()[0].get_text()))
        self.builderListBox.add(row)
        print(self.amode["AutonomousModes"][self.selected_auto]["Commands"])
        self.show_all()

    def on_command_up_clicked(self, widget):
        print("up")
        if self.command_location > 0:
            temp = self.amode["AutonomousModes"][
                self.selected_auto]["Commands"][self.command_location]
            self.amode["AutonomousModes"][self.selected_auto]["Commands"][
                self.command_location] = self.amode["AutonomousModes"][
                    self.selected_auto]["Commands"][self.command_location - 1]
            self.amode["AutonomousModes"][self.selected_auto]["Commands"][
                self.command_location - 1] = temp
            self.command_location -= 1
            for row in self.builderListBox.get_children():
                row.destroy()
            for i in self.amode["AutonomousModes"][
                    self.selected_auto]["Commands"]:
                row = Gtk.ListBoxRow()
                label = Gtk.Label()
                label.set_text(i["Name"])
                row.add(label)
                self.builderListBox.add(row)
                self.show_all()
            self.builderListBox.select_row(
                self.builderListBox.get_row_at_index(self.command_location))
            self.on_amode_command_selected(self, self.builderListBox)

    def on_command_down_clicked(self, widget):
        print("down")
        if self.command_location < len(self.amode["AutonomousModes"][
                self.selected_auto]["Commands"]) - 1:
            temp = self.amode["AutonomousModes"][
                self.selected_auto]["Commands"][self.command_location]
            self.amode["AutonomousModes"][self.selected_auto]["Commands"][
                self.command_location] = self.amode["AutonomousModes"][
                    self.selected_auto]["Commands"][self.command_location + 1]
            self.amode["AutonomousModes"][self.selected_auto]["Commands"][
                self.command_location + 1] = temp
            self.command_location += 1
            for row in self.builderListBox.get_children():
                row.destroy()
            for i in self.amode["AutonomousModes"][
                    self.selected_auto]["Commands"]:
                row = Gtk.ListBoxRow()
                label = Gtk.Label()
                label.set_text(i["Name"])
                row.add(label)
                self.builderListBox.add(row)
                self.show_all()
            self.builderListBox.select_row(
                self.builderListBox.get_row_at_index(self.command_location))
            self.on_amode_command_selected(self, widget)

    def on_remove_command_clicked(self, widget):
        print("remove")
        self.amode["AutonomousModes"][self.selected_auto]["Commands"].pop(
            self.command_location)
        for row in self.builderListBox.get_children():
            row.destroy()
        for i in self.amode["AutonomousModes"][self.selected_auto]["Commands"]:
            row = Gtk.ListBoxRow()
            label = Gtk.Label()
            label.set_text(i["Name"])
            row.add(label)
            self.builderListBox.add(row)
            self.show_all()
        if self.command_location > 0:
            self.command_location -= 1
            self.builderListBox.select_row(
                self.builderListBox.get_row_at_index(self.command_location))
            self.on_amode_command_selected(self, self.builderListBox)
        else:
            self.paramsListBox.foreach(lambda x: x.destroy())
            self.show_all()

    def on_add_amode_clicked(self, widget):
        print("add amode")
        self.amode["AutonomousModes"].append({
            "Name": "New Mode",
            "Commands": []
        })
        row = Gtk.ListBoxRow()
        row.add(Gtk.Label("New Mode"))
        self.amodeListBox.add(row)
        self.selected_auto = len(self.amode["AutonomousModes"]) - 1
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
            self.amode["AutonomousModes"][
                self.selected_auto]["Name"] = entry.get_text()
            self.amodeListBox.get_selected_rows()[0].get_child().set_text(
                entry.get_text())
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
        scrolled.add(Gtk.Label(json.dumps(self.amode, indent=2)))
        dialog.get_content_area().add(scrolled)
        dialog.show_all()
        response = dialog.run()
        if (response == Gtk.ResponseType.OK):
            dialog.destroy()

    def aboutPage(self, widget):
        about = Gtk.AboutDialog()
        about.set_program_name("Autonomous Mode Builder")
        about.set_version("1.0")
        about.set_comments(
            "This is a tool to help build autonomous modes for team 238's robot."
        )
        about.set_website("frc238.org")
        about.show_all()
        response = about.run()


win = amodeWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

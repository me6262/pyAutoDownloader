import re
import os
import json
# path = '/home/haydenm/Documents/workspaces/238_2022_Baseline/src/main/java/frc/robot/commands'
command_reg = '.*/(.*).java'
annot_reg = '@AutonomousModeAnnotation\(parameterNames = {(.*)}\)'
path_reg = '.*/(.*)\.path'
rg = re.compile(annot_reg, re.IGNORECASE)
rf = re.compile(command_reg, re.IGNORECASE)
rp = re.compile(path_reg)
all_commands = []
all_trajectories = []
list_of_cmd_files = []
list_of_traj_files = []

js = []


def get_commands(path):
    command_path = path + "/src/main/java/frc/robot/commands"
    for root, dirs, files in os.walk(command_path):
        for file in files:
            list_of_cmd_files.append(os.path.join(root, file))
    for name in list_of_cmd_files:
        readfile = open(name)
        lines = readfile.readlines()
        f = rf.search(name)
        
        for line in lines:
            m = rg.search(line)
            if m:
                all_commands.append({"Command": [{"Name": f.group(1)}, {"params": m.group(1).replace('"', "").strip().split(',')}]})
    return all_commands

def get_trajectories(path):
    trajec_path = path + "/src/main/deploy/pathplanner"
    for root, dirs, files in os.walk(trajec_path):
        for file in files:
            list_of_traj_files.append(os.path.join(root, file))
    for name in list_of_traj_files:
        m = rp.search(name)
        if m:
            all_trajectories.append(m.group(1))
            print(m.group(0))
    return all_trajectories
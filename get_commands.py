import re
import os
import json
path = '/home/haydenm/Documents/workspaces/238_2022_Baseline/src/main/java/frc/robot/commands'
command_reg = '.*/(.*).java'
annot_reg = '@AutonomousModeAnnotation\(parameterNames = {(.*)}\)'
rg = re.compile(annot_reg, re.IGNORECASE)
rf = re.compile(command_reg, re.IGNORECASE)
all_commands = []
list_of_files = []
js = []

for root, dirs, files in os.walk(path):
    for file in files:
        list_of_files.append(os.path.join(root, file))
for name in list_of_files:
    readfile = open(name)
    lines = readfile.readlines()
    f = rf.search(name)
    
    for line in lines:
        m = rg.search(line)
        if m:
            all_commands.append({"Command": [{"Name": f.group(1)}, {"params": [m.group(1).replace('"', "").strip()]}]})
print(json.dumps(all_commands))

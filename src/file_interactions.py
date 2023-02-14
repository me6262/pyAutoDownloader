import os


def get_last_project_path(perms):
    project_root = os.path.dirname(os.path.dirname(__file__))
    if os.name == "nt":
        return open(project_root + "\\savedata\\prevNTPath.txt", perms)
    else:
        return open(project_root + "/savedata/prevFilepath.txt", perms)



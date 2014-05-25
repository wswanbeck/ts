import os
import sys
import inspect


# Based on: http://stackoverflow.com/questions/279237/import-a-module-from-a-folder
def add_path(reldir):
    cmd_folder = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
    add_dir = os.path.normpath(os.path.join(cmd_folder, reldir))
    if add_dir not in sys.path:
        sys.path.append(add_dir)


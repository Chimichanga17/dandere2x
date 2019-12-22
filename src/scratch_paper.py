"""
Start the dandere2x_gui_wrapper class using the .yaml. Essentially, use this if you want to
simulate d2x being started from the gui w/o having to actually use the GUI.

Starting from this driver will do stuff the GUI will do, such as delete the workspace, and other functions
if decided on by the user.
"""

import time

import yaml

from dandere2xlib.utils.dandere2x_utils import get_operating_system
from wrappers.dandere2x_gui_wrapper import Dandere2x_Gui_Wrapper
from wrappers.dandere2x_cpp import Dandere2xCppWrapper
from context import Context

def main():
    start = time.time()

    # get config based on OS
    # configfile = "dandere2x_%s.yaml" % get_operating_system()
    #
    # # load yaml
    #
    # with open(configfile, "r") as read_file:
    #     config = yaml.safe_load(read_file)
    #
    # context = Context(config)
    #
    # d2xcpp = Dandere2xCppWrapper(context)
    # d2xcpp.run()
    import threading
    print(threading.enumerate())



if __name__ == "__main__":
    main()

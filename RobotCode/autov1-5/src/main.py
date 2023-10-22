# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Joshua                                                       #
# 	Created:      10/11/2023, 6:30:21 PM                                       #
# 	Description:  IQ2 project                                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()
leftdrive = Motor(Ports.PORT6,True)
rightdrive = Motor(Ports.PORT1,False)
rightbeam = Motor(Ports.PORT4,True)
leftbeam = Motor(Ports.PORT2,False)
intake = Motor(Ports.PORT3)
dt = DriveTrain(leftdrive,rightbeam)


def start():
    dt.drive(FORWARD)
start()
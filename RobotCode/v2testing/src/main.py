# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Joshua                                                       #
# 	Created:      10/4/2023, 5:31:34 PM                                        #
# 	Description:  IQ2 project                                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain = Brain()
rightdrive = Motor(Ports.PORT1,1.0,True)
leftdrive = Motor(Ports.PORT6,1.0,False)
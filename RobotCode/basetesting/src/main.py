
from vex import *
import urandom

# Brain should be defined by default
brain = Brain()

from vex import *

# locking
locktimer = 120
MAXIMUIMTIMER = 120
locked = False
inputs = False

# define eletronics
brain = Brain()
controller = Controller()
Right_Drive = Motor(Ports.PORT6,1.5,True)
Left_Drive = Motor(Ports.PORT1,1.5,True)
Internal = Inertial()
drivebase = SmartDrive(Left_Drive, Right_Drive, Internal, 200)
dumperRight = Motor(Ports.PORT2,1,False)
dumperLeft = Motor(Ports.PORT3,1,True)
dumper = MotorGroup(dumperLeft,dumperRight)
intake = Motor(Ports.PORT4,1,False)
Rstop = False
Lstop = False
slow = False
sensitivity = 2

#controllerCode
def controllerloop():
    global Rstop, Lstop, Right_Drive, Left_Drive, controller, brain, inputs
    while True:
        driveleftspeed = controller.axisC.position() - controller.axisA.position()
        driverightspeed = controller.axisC.position() + controller.axisA.position() 
        
        if driveleftspeed < sensitivity and driveleftspeed > -sensitivity:
            if Lstop:
                inputs = True
                Left_Drive.stop()
                Lstop = False
        else:
            Lstop = True
        if driverightspeed < sensitivity and driverightspeed > -sensitivity:
            if Rstop:
                inputs = True
                Right_Drive.stop()
                Rstop = False
        else:
            Rstop = True

        if Lstop:
            inputs = True
            Left_Drive.set_velocity(driveleftspeed,PERCENT)
            Left_Drive.set_max_torque(100,PERCENT)
            Left_Drive.spin(FORWARD)
        if Rstop:
            inputs = True
            Right_Drive.set_velocity(driverightspeed,PERCENT)
            Left_Drive.set_max_torque(100,PERCENT)
            Right_Drive.spin(FORWARD)
        wait(20,MSEC)


def ticktimer():
    global locktimer, MAXIMUMTIMER, locked, inputs
    while True:
        if locked == False:
            locktimer -= 1
            if inputs == True:
                locktimer = MAXIMUMTIMER
            else:
                if locktimer == 0:
                        locked = True
            
        else:
            break
        wait(1,SECONDS)

Thread(ticktimer)
Thread(controllerloop)
intakeactive = False
intake.set_velocity(80,PERCENT)
intake.set_max_torque(100,PERCENT)
def toggleintake():
    wait(1,MSEC)
    global intakeactive, inputs
    inputs = True
    if intakeactive:
        intakeactive = False
        intake.spin(FORWARD)
    else:
        intakeactive = True
        intake.spin(REVERSE)
    inputs = False

def dumperup():
    wait(1,MSEC)
    global inputs
    inputs = True
    dumper.spin(FORWARD)

def dumperdown():
    wait(1,MSEC)
    global inputs
    inputs = True
    dumper.spin(REVERSE)

def dumperstop():
    wait(1,MSEC)
    global inputs
    inputs = True
    dumper.stop()

def intakestop():
    wait(1,MSEC)
    global inputs
    inputs = True
    intake.stop()

def slowmode():
    wait(1,MSEC)
    global inputs, ssensitivity, slow
    inputs = True
    if slow == False:
        slow = True
        sensitivity = 20
    else:
        slow = False
        sensitivity = 2


dumper.set_max_torque(100,PERCENT)
dumper.set_velocity(80,PERCENT)
dumper.set_position(0,DEGREES)
dumper.set_stopping(HOLD)
controller.buttonFUp.pressed(slowmode)
controller.buttonRUp.pressed(toggleintake)
controller.buttonLUp.pressed(dumperup)
controller.buttonLDown.pressed(dumperdown)
controller.buttonRDown.pressed(intakestop)
controller.buttonLUp.released(dumperstop)
controller.buttonLDown.released(dumperstop)
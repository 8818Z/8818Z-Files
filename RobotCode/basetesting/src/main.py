
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

from vex import *

# define eletronics
brain = Brain()
controller = Controller()
Right_Drive = Motor(Ports.PORT6,1.5,True)
Left_Drive = Motor(Ports.PORT1,1.5,True)
Internal = Inertial()
drivebase = SmartDrive(Left_Drive, Right_Drive, Internal, 200)
dumperRight = Motor(Ports.PORT2,1,False)
dumperLeft = Motor(Ports.PORT3,1,False)
dumper = MotorGroup(dumperLeft,dumperRight)
intake = Motor(Ports.PORT4,1,False)
Rstop = False
Lstop = False
sensitivity = 5
def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Inertial")
    Internal.calibrate()
    while Internal.is_calibrating():
        sleep(25, MSEC)
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)

calibrate_drivetrain()
#controllerCode
def controllerloop():
    global Rstop, Lstop, Right_Drive, Left_Drive, controller, brain
    while True:
        driveleftspeed = controller.axisC.position() - controller.axisA.position()
        driverightspeed = controller.axisC.position() + controller.axisA.position() 
        
        if driveleftspeed < sensitivity and driveleftspeed > -sensitivity:
            if Lstop:
                Left_Drive.stop()
                Lstop = False
        else:
            Lstop = True
        if driverightspeed < sensitivity and driverightspeed > -sensitivity:
            if Rstop:
                Right_Drive.stop()
                Rstop = False
        else:
            Rstop = True

        if Lstop:
            Left_Drive.set_velocity(driveleftspeed,PERCENT)
            Left_Drive.spin(FORWARD)
        if Rstop:
            Right_Drive.set_velocity(driverightspeed,PERCENT)
            Right_Drive.spin(FORWARD)
        wait(20,MSEC)




Thread(controllerloop)
intakeactive = False
intake.set_velocity(100,PERCENT)
intake.set_max_torque(100,PERCENT)
def toggleintake():
    global intakeactive
    if intakeactive:
        intakeactive = False
        intake.spin(FORWARD)
    else:
        intakeactive = True
        intake.spin(REVERSE)
def dumperup():
    intake.spin(REVERSE)
    dumper.spin(FORWARD)

def dumperdown():
    intake.spin(FORWARD)
    dumper.spin(REVERSE)

def dumperstop():
    dumper.stop()
dumper.set_max_torque(100,PERCENT)
dumper.set_position(0,DEGREES)
dumper.set_stopping(HOLD)
controller.buttonRUp.pressed(toggleintake)

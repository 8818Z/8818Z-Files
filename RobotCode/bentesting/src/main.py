
# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()
rightdrive = Motor(Ports.PORT1,False)
leftdrive = Motor(Ports.PORT6,True)
Beam1 = Motor(Ports.PORT2,True)
Beam2 = Motor(Ports.PORT3,False)
beams = MotorGroup(Beam1,Beam2)
Intake = Motor(Ports.PORT4)
controller = Controller()
intakestatus = "in"
Intake.set_max_torque(999999,PERCENT)
Intake.set_velocity(99999,PERCENT)

# def setRandomSeedUsingAccel():
#     wait(100, MSEC)
#     xaxis = brain_inertial.acceleration(XAXIS) * 1000
#     yaxis = brain_inertial.acceleration(YAXIS) * 1000
#     zaxis = brain_inertial.acceleration(ZAXIS) * 1000
#     urandom.seed(int(xaxis + yaxis + zaxis))
    
# # Set random seed 
#setRandomSeedUsingAccel()



# define variables used for controlling motors based on controller inputs
drivetrain_l_needs_to_be_stopped_controller = False
drivetrain_r_needs_to_be_stopped_controller = False

# define a task that will handle monitoring inputs from controller
def rc_auto_loop_function_controller():
    global drivetrain_l_needs_to_be_stopped_controller, drivetrain_r_needs_to_be_stopped_controller, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axisA + axisC
            # right = axisA - axisC
            drivetrain_left_side_speed = controller.axisA.position() + controller.axisC.position()
            drivetrain_right_side_speed = controller.axisA.position() - controller.axisC.position()
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller:
                    # stop the left drive motor
                    leftdrive.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller:
                    # stop the right drive motor
                    rightdrive.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller:
                leftdrive.set_velocity(drivetrain_left_side_speed, PERCENT)
                leftdrive.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller:
                rightdrive.set_velocity(drivetrain_right_side_speed, PERCENT)
                rightdrive.spin(FORWARD)
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller = Thread(rc_auto_loop_function_controller)
def toggleintake():
    global intakestatus
    if intakestatus == "out":
        intakestatus = "in"
        Intake.spin(REVERSE)
    else:
        intakestatus = "out"
        Intake.spin(FORWARD)
def stopintake():
    global intakestatus
    Intake.stop()
    intakestatus = "in"

def armup():
    beams.spin(FORWARD)
def armdown():
    beams.spin(REVERSE)
def armstop():
    beams.stop()
beams.set_stopping(BrakeType.HOLD)
controller.buttonLUp.pressed(armup)
controller.buttonLDown.pressed(armdown)
controller.buttonLUp.released(armstop)
controller.buttonLDown.released(armstop)
controller.buttonRDown.pressed(stopintake)
controller.buttonRUp.pressed(toggleintake)
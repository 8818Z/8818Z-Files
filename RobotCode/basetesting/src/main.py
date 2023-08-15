

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

# Robot configuration code
brain_inertial = Inertial()
controller = Controller()
left_drive_smart = Motor(Ports.PORT1, 1, False)
right_drive_smart = Motor(Ports.PORT6, 1, True)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 200, 173, 76, MM, 1)
intake = Motor(Ports.PORT2,1,False)
intakeactive = False
drivetrain_l_needs_to_be_stopped_controller = False
drivetrain_r_needs_to_be_stopped_controller = False
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
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < -5 and drivetrain_right_side_speed > 5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller = Thread(rc_auto_loop_function_controller)
def toggleintake():
    print("tset")
    brain.screen.print("yeses")
    global intakeactive
    if not intakeactive:
        intakeactive = True
        intake.spin(FORWARD)
        intake.set_velocity(55,PERCENT)
        intake.set_max_torque(100,PERCENT)
    else:
        intakeactive = False
        intake.spin(REVERSE)
brain.screen.print("yes")
controller.buttonRUp.pressed(toggleintake)


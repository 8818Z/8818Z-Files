
from vex import *


# square side: 35 cm

# Brain should be defined by default
brain=Brain()

#DriveStuff
RightDrive = Motor(Ports.PORT1)
LeftDrive = Motor(Ports.PORT6)
Drive = DriveTrain(LeftDrive,RightDrive)


class squareregion:
    def __init__(self, amountX, amountY) -> None:
        self.X = amountX * 35 + 20
        self.Y = amountY * 35 + 20
        self.magnitude = ((self.X ** 2) + (self.Y ** 2))
        
    def clear(self):
        self = None

class squaredrive:
    def __init__(self) -> None:
        print("Drivetraininit")
    def drivefor(self, squareregion, Direction) -> None:
        Drive.drive_for(Direction, squareregion.Y)
        while not Drive.is_moving() == False:
            wait(0, MSEC)
        squareregion.clear()

square = squaredrive()

square.drivefor(squareregion(0,1), FORWARD)
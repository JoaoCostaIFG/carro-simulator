from enum import Enum


class CarroTransition(Enum):
    ParkingBrake = 0
    UnparkingBrake = 1
    BeganDriving = 2
    Stopped = 3

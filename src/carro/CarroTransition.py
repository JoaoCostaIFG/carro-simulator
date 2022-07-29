from enum import IntEnum


class CarroTransition(IntEnum):
    ParkingBrake = 0
    UnparkingBrake = 1
    BeganDriving = 2
    Stopped = 3

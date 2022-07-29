from enum import IntEnum

from carro.CarroTransition import CarroTransition


class CarroState(IntEnum):
    Invalid = 0
    Parked = 1
    Ready = 2
    Driving = 3

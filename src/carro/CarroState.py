from enum import Enum

from carro.CarroTransition import CarroTransition


class CarroState(Enum):
    Invalid = -1
    Parked = 0
    Ready = 1
    Driving = 2

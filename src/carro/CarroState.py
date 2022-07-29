from enum import Enum

from carro.CarroTransition import CarroTransition


class CarroState(Enum):
    Invalid = 0
    Parked = 1
    Ready = 2
    Driving = 3

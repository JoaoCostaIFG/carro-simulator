import BrakeSystem
import CarroState
import Engine


class Carro:
    state: CarroState = CarroState.Parked
    weight: int = 1500  # in Kg

    brakeSystem: BrakeSystem = BrakeSystem()
    engine: Engine = Engine()

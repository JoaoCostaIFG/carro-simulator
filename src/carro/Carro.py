import BrakeSystem
import CarroState
import Engine


class Carro:
    state: CarroState = CarroState.Parked
    weight: int = 1500  # in Kg
    parkingBrakeState: bool = True  # False - not active || True - active

    brakeSystem: BrakeSystem = BrakeSystem()
    engine: Engine = Engine()

    def setParkingBrakeState(self, state):
        self.parkingBrakeState = state

    def getParkingBrakeState(self):
        return self.parkingBrakeState

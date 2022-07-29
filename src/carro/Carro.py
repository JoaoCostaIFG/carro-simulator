import BrakeSystem
import CarroState
import Engine
from carro.CarroTransition import CarroTransition


class Carro:
    state: CarroState = CarroState.Parked
    weight: int = 1500  # in Kg
    parkingBrakeState: bool = True  # False - not active || True - active

    brakeSystem: BrakeSystem = BrakeSystem()
    engine: Engine = Engine()

    transitions = [
        # ParkingBrake       UnparkingBrake
        [CarroState.Invalid, CarroState.Invalid],  # Invalid
        [CarroState.Parked, CarroState.Ready],  # Parked
        [CarroState.Invalid, CarroState.Invalid],  # Ready
        [CarroState.Invalid, CarroState.Invalid],  # Driving
    ]

    def transition(self, trans) -> CarroState:
        newState: CarroState = self.transitions[self.state][trans]
        return newState

    def setParkingBrakeState(self, state):
        trans: CarroState = CarroTransition.ParkingBrake
        if self.parkingBrakeState and not state:
            trans = CarroTransition.UnparkingBrake

        if self.transition(trans) == CarroState.Invalid:
            # TODO THIS IS BAD => warn user
            return False
        self.parkingBrakeState = state
        return True

    def getParkingBrakeState(self):
        return self.parkingBrakeState

from carro.BrakeSystem import BrakeSystem
from carro.Engine import Engine
from carro.CarroState import CarroState
from carro.CarroTransition import CarroTransition


class Carro:
    weight: int = 1500  # Kg
    maxSpeed: float = 250  # km/h

    transitions = [
        # ParkingBrake       UnparkingBrake
        [CarroState.Invalid, CarroState.Invalid],  # Invalid
        [CarroState.Parked, CarroState.Ready],  # Parked
        [CarroState.Parked, CarroState.Ready],  # Ready
        [CarroState.Invalid, CarroState.Invalid],  # Driving
    ]

    def __init__(self) -> None:
        self.brakeSystem: BrakeSystem = BrakeSystem()
        self.engine: Engine = Engine()

        self.state: CarroState = CarroState.Parked
        self.parkingBrakeState: bool = True  # False - not active || True - active
        self.speed: float = 0.0  # km/h

    def transition(self, trans: CarroTransition) -> CarroState:
        newState: CarroState = self.transitions[self.state][trans]
        return newState

    def setParkingBrakeState(self, state: CarroState) -> bool:
        trans: CarroState = CarroTransition.ParkingBrake
        if self.parkingBrakeState and not state:
            trans = CarroTransition.UnparkingBrake

        if self.transition(trans) == CarroState.Invalid:
            # TODO THIS IS BAD => warn user
            return False
        self.parkingBrakeState = state
        return True

    def getParkingBrakeState(self) -> bool:
        return self.parkingBrakeState

    def getSpeed(self) -> float:
        return self.speed

    def setAccelerationPedal(self, val: int) -> None:
        return self.engine.setPedal(val)

    def update(self, deltaTime: float) -> None:
        # update car speed (care for m/s to km/h conversion)
        deltaSpeed: float = deltaTime * (
            self.engine.getAcceleration() - self.brakeSystem.getDeceleration()
        )
        self.speed += deltaSpeed * 3.6  # 0.001 / (1/3600)
        # clamp
        self.speed = min(max(0.0, self.speed), Carro.maxSpeed)

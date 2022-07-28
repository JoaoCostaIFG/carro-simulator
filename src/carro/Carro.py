import sys

from carro.BrakeSystem import BrakeSystem
from carro.Engine import Engine
from carro.CarroState import CarroState
from carro.CarroTransition import CarroTransition


class Carro:
    weight: int = 1500  # Kg
    maxSpeed: float = 250  # km/h

    # fmt: off
    transitions = [
        # ParkingBrake          UnparkingBrake      BeganDriving        Stopped
        [CarroState.Invalid,    CarroState.Invalid, CarroState.Invalid, CarroState.Invalid],    # Invalid
        [CarroState.Parked,     CarroState.Ready,   CarroState.Invalid, CarroState.Parked],     # Parked
        [CarroState.Parked,     CarroState.Ready,   CarroState.Driving, CarroState.Ready],      # Ready
        [CarroState.Invalid,    CarroState.Driving, CarroState.Driving, CarroState.Ready],      # Driving
    ]
    # fmt: on

    def __init__(self) -> None:
        self.brakeSystem: BrakeSystem = BrakeSystem()
        self.engine: Engine = Engine()

        self.state: CarroState = CarroState.Parked
        self.parkingBrakeState: bool = True  # False - not active || True - active
        self.speed: float = 0.0  # km/h
        self.timeStopped: float = 0.0  # s

    def transition(self, trans: CarroTransition) -> CarroState:
        newState: CarroState = Carro.transitions[self.state.value][trans.value]
        if self.state != CarroState.Invalid:
            self.state = newState
        else:
            print(
                f"State transition is invalid: [state={self.state}], [transition={trans}]",
                file=sys.stderr,
            )
        return newState

    def setParkingBrakeState(self, brakeState: bool) -> bool:
        trans: CarroState = CarroTransition.ParkingBrake
        if self.parkingBrakeState and not brakeState:
            trans = CarroTransition.UnparkingBrake

        if self.transition(trans) == CarroState.Invalid:
            return False
        self.parkingBrakeState = brakeState
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

        if self.speed == 0.0:
            self.timeStopped += deltaTime
            if self.timeStopped >= 30.0:
                self.transition(CarroTransition.Stopped)
        else:
            self.timeStopped = 0.0
            if self.speed > 10.0:
                self.transition(CarroTransition.BeganDriving)

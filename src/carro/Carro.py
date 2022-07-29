from sys import stderr

import can

from carro.BrakeSystem import BrakeSystem
from carro.Engine import Engine
from carro.CarroState import CarroState
from carro.CarroTransition import CarroTransition
from messages.SimMessage import SimMessage


class Carro:
    _weight: int = 1500  # Kg
    _maxSpeed: float = 250  # km/h

    # fmt: off
    _transitions = [
        # ParkingBrake          UnparkingBrake      BeganDriving        Stopped
        [CarroState.Invalid,    CarroState.Invalid, CarroState.Invalid, CarroState.Invalid],    # Invalid
        [CarroState.Parked,     CarroState.Ready,   CarroState.Invalid, CarroState.Parked],     # Parked
        [CarroState.Parked,     CarroState.Ready,   CarroState.Driving, CarroState.Ready],      # Ready
        [CarroState.Invalid,    CarroState.Driving, CarroState.Driving, CarroState.Ready],      # Driving
    ]
    # fmt: on

    def __init__(self) -> None:
        self._brakeSystem: BrakeSystem = BrakeSystem()
        self._engine: Engine = Engine()

        self._state: CarroState = CarroState.Parked
        self._parkingBrakeState: bool = True  # False - not active || True - active
        self._speed: float = 0.0  # km/h
        self._timeStopped: float = 0.0  # s

    @property
    def state(self) -> CarroState:
        return self._state

    @property
    def parkingBrake(self) -> bool:
        return self._parkingBrakeState

    @parkingBrake.setter
    def parkingBrake(self, brakeState: bool) -> None:
        trans: CarroState = CarroTransition.ParkingBrake
        if self._parkingBrakeState and not brakeState:
            trans = CarroTransition.UnparkingBrake

        if self.transition(trans) == CarroState.Invalid:
            raise ValueError("Can't activate the parking brake right now.")
        self._parkingBrakeState = brakeState

    @property
    def speed(self) -> float:
        return self._speed

    @property
    def engine(self) -> Engine:
        return self._engine

    @property
    def brake(self) -> BrakeSystem:
        return self._brakeSystem

    def transition(self, trans: CarroTransition) -> CarroState:
        newState: CarroState = Carro._transitions[self._state.value][trans.value]
        if self._state != CarroState.Invalid:
            self._state = newState
        else:
            print(
                f"State transition is invalid: [state={self._state}], [transition={trans}]",
                file=stderr,
            )
        return newState

    def update(self, deltaTime: float) -> None:
        # update car speed (care for m/s to km/h conversion)
        if self._state == CarroState.Ready or self._state == CarroState.Driving:
            deltaSpeed: float = deltaTime * (
                self._engine.acceleration - self._brakeSystem.deceleration
            )
            newSpeed: float = self._speed + deltaSpeed * 3.6  # 0.001 / (1/3600)
            # clamp
            self._speed = min(max(0.0, newSpeed), Carro._maxSpeed)

        if self._speed == 0.0:
            self._timeStopped += deltaTime
            if self._timeStopped >= 30.0:
                self.transition(CarroTransition.Stopped)
        else:
            self._timeStopped = 0.0
            if self._speed > 10.0:
                self.transition(CarroTransition.BeganDriving)

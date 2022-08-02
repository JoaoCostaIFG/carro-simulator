import pytest
from carro.Carro import Carro
from carro.CarroState import CarroState
from carro.CarroTransition import CarroTransition

MARGIN : int = 0.2

class TestCar:
    car : Carro = Carro()

    @pytest.fixture(autouse=True)
    def before_each(self):
        self.car = Carro()

    def test_weigth(self):
        assert self.car._weight == 1500

    def test_initial_pedals(self):
        assert self.car._engine.pedal == 0
        assert self.car._brakeSystem.pedal == 0
        assert self.car._parkingBrakeState == True

    def test_initial_oper_mode(self):
        assert self.car.state == CarroState.Parked

    def test_transitions(self):
        # REQ-07
        self.car.parkingBrake = False
        assert self.car.state == CarroState.Ready

        # REQ-08
        self.car.setAcceleration(3)
        self.car.update(2)
        finalSpeed : float = 3 * 2 * 3.6
        assert self.car.speed - finalSpeed < MARGIN
        assert self.car.state == CarroState.Driving

        # REQ-09
        self.car.setAcceleration(-3)
        self.car.update(2.5)

        self.car.update(31)
        assert self.car.speed < MARGIN
        assert self.car.state == CarroState.Ready

        # REQ-10
        self.car.parkingBrake = True
        assert self.car.state == CarroState.Parked

    def test_invalid_transitions(self):
        assert self.car._transitions[CarroState.Parked.value][CarroTransition.BeganDriving.value] == CarroState.Invalid
        assert self.car._transitions[CarroState.Driving.value][CarroTransition.ParkingBrake.value] == CarroState.Invalid

    def test_accel_rpm(self):
        # The car engine shall produce the maximum acceleration of 5 m/s2 at 8000rpm.
        self.car.setAcceleration(self.car.engine.maxAcceleration)
        assert self.car.engine.rpm == self.car.engine.maxRpm 

    def test_accel_pedal(self):
        # The car engine produced acceleration shall be vary linearly with the accelerator pedal position.
        self.car.acceleration

    def test_set_negative_accel(self):
        accelValue : int = 1
        self.car.setAcceleration(-accelValue)

        assert self.car.engine.pedal == 0
        assert abs(self.car._brakeSystem.deceleration - accelValue) < MARGIN

    def test_set_positive_accel(self):
        accelValue : int = 1
        self.car.setAcceleration(accelValue)

        assert self.car._brakeSystem.pedal == 0
        assert abs(self.car.engine.acceleration - accelValue) < MARGIN
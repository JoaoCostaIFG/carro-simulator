from carro.Carro import Carro
from carro.CarroState import CarroState
from carro.CarroTransition import CarroTransition

MARGIN : int = 0.2

class TestCar:
    car : Carro = Carro()

    def test_weigth(self):
        assert self.car._weight == 1500

    def test_initial_pedals(self):
        assert self.car._engine.pedal == 0
        assert self.car._brakeSystem.pedal == 0
        assert self.car._parkingBrakeState == True

    def test_initial_oper_mode(self):
        assert self.car.state == CarroState.Parked

    # def test_transitions(self):
        # Parking brake setter changes the state


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
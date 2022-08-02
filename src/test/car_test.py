from carro.Carro import Carro

MARGIN : int = 0.2

class TestCar:
    car : Carro = Carro()

    def test_set_negative_accel(self):
        accelValue : int = 1
        self.car.setAcceleration(-accelValue)


        assert self.car.engine.pedal == 0
        assert abs(self.car._brakeSystem.deceleration - accelValue) < MARGIN
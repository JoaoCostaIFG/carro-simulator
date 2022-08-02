from math import ceil


class Engine:
    _maxAcceleration: float = 5  # m/s^2
    _maxRPM: int = 8000

    def __init__(self) -> None:
        self._pedal: int = 0  # 0 - not acceleration || 100 - max acceleration

    @property
    def pedal(self) -> int:
        return self._pedal

    @pedal.setter
    def pedal(self, val: int) -> None:
        if val < 0 or val > 100:
            raise ValueError("Pedal value must be in interval [0, 100].")
        self._pedal = int(val)

    @property
    def acceleration(self) -> float:
        return Engine._maxAcceleration * (self._pedal / 100.0)

    @acceleration.setter
    def acceleration(self, val: float) -> None:
        if val <= 0:
            self._pedal = 0
            return
        self._pedal = min(ceil(val / Engine._maxAcceleration * 100), 100)

    @property
    def rpm(self) -> int:
        return round(Engine._maxRPM * (self._pedal / 100.0))
    
    @property
    def maxRpm(self) -> int:
        return self._maxRPM
    
    @property
    def maxAcceleration(self) -> int:
        return self._maxAcceleration


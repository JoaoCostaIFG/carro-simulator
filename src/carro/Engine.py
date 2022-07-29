class Engine:
    _maxAcceleration: float = 5  # m/s^2
    _maxRPM: int = 8000

    def __init__(self) -> None:
        self._pedal: int = 0  # 0 - not acceleration || 100 - max acceleration

    # TODO setter
    def setPedal(self, val: int) -> None:
        assert val >= 0 and val <= 100
        self._pedal = val

    @property
    def acceleration(self) -> float:
        return Engine._maxAcceleration * (self._pedal / 100.0)

    @property
    def rpm(self) -> float:
        return Engine._maxRPM * (self._pedal / 100.0)

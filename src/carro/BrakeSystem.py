from math import ceil


class BrakeSystem:
    _maxDeceleration: float = 6  # m/s^2

    def __init__(self) -> None:
        self._pedal: int = 0  # 0 - unactioned || 100 - fully actioned

    @property
    def pedal(self) -> int:
        return self._pedal

    @pedal.setter
    def pedal(self, val: int) -> None:
        if val < 0 or val > 100:
            raise ValueError("Pedal value must be in interval [0, 100].")
        self._pedal = int(val)

    @property
    def deceleration(self) -> float:
        return BrakeSystem._maxDeceleration * (self._pedal / 100.0)

    @deceleration.setter
    def deceleration(self, val: float) -> None:
        if val <= 0:
            self._pedal = 0
            return
        self._pedal = min(ceil(val / BrakeSystem._maxDeceleration * 100), 100)

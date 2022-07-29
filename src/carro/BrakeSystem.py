class BrakeSystem:
    _maxDeceleration: float = 6  # m/s^2

    def __init__(self) -> None:
        self._pedal: int = 0  # 0 - unactioned || 100 - fully actioned

    # TODO setter
    def setPedal(self, val: int) -> None:
        # TODO exception
        assert val >= 0 and val <= 100
        self._pedal = val

    @property
    def deceleration(self) -> float:
        return BrakeSystem._maxDeceleration * (self._pedal / 100.0)

class BrakeSystem:
    maxDeceleration: float = 6  # m/s^2

    def __init__(self) -> None:
        self.pedal: int = 0  # 0 - unactioned || 100 - fully actioned

    def setPedal(self, val: int) -> None:
        assert val >= 0 and val <= 100
        self.pedal = val

    def getDeceleration(self) -> float:
        return BrakeSystem.maxDeceleration * (self.pedal / 100.0)

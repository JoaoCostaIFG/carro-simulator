class BrakeSystem:
    maxDeceleration: float = 6  # m/s^2
    pedal: int = 0  # 0 - unactioned || 100 - fully actioned

    def setPedal(self, val):
        assert val >= 0 and val <= 100
        self.pedal = val

    def getDecelation(self):
        return self.maxDeceleration * (self.pedal / 100.0)

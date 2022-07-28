class Engine:
    maxAcceleration: float = 5  # m/s^2
    maxRPM: int = 8000
    pedal: int = 0  # 0 - not acceleration || 100 - max acceleration

    def setPedal(self, val):
        assert val >= 0 and val <= 100
        self.pedal = val

    def getAcceleration(self):
        return self.maxAcceleration * (self.pedal / 100.0)

    def getRPM(self):
        return self.maxRPM * (self.pedal / 100.0)

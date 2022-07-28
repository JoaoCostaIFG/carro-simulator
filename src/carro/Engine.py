class Engine:
    maxAcceleration: float = 5  # m/s^2
    maxRPM: int = 8000

    def __init__(self) -> None:
        self.pedal: int = 0  # 0 - not acceleration || 100 - max acceleration

    def setPedal(self, val: int) -> None:
        assert val >= 0 and val <= 100
        self.pedal = val

    def getAcceleration(self) -> float:
        return Engine.maxAcceleration * (self.pedal / 100.0)

    def getRPM(self) -> float:
        return Engine.maxRPM * (self.pedal / 100.0)

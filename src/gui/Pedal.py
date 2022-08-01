class Pedal:
    def __init__(self) -> None:
        # 0 -> not pressed. 100 -> fully pressed
        self._position: int = 0

    @property
    def position(self) -> int:
        return self._position

    @position.setter
    def position(self, newPos: int):
        if newPos >= 0 and newPos <= 100:
            self._position = int(newPos)

    def setPosition(self, newPos: int):
        if newPos >= 0 and newPos <= 100:
            self.position = newPos
    
    def incrementPos(self):
        if self._position >= 0 and self._position < 100:
            self.position += 1
    
    def decrementPos(self):
        if self._position > 0 and self._position <= 100:
            self.position -= 1

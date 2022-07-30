class Pedal:
    def __init__(self) -> None:
        # 0 -> not pressed. 100 -> fully pressed
        self._position: int = 0

    @property
    def position(self) -> int:
        return self._position

    @position.setter
    def position(self, newPos: int):
        self._position = newPos
        print("Changing Position of pedal to -> " + str(newPos))

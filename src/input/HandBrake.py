class HandBrake:
    def __init__(self) -> None:
        self._active: bool = True

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, newValue: bool):
        self._active = newValue
        print("Changing hand brake to -> " + str(newValue))

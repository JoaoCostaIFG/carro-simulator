class HandBrake:
    def __init__(self) -> None:
        self._active: bool = True

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, newValue: bool):
        self._active = newValue

    def setActive(self, newValue: bool):
        self.active = newValue

    def toggleActive(self):
        self.active = not self.active

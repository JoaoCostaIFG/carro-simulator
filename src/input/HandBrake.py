class HandBrake:
    active: bool = True

    def setActive(self, newValue: bool):
        self.active = newValue
        print("Changing hand brake to -> " + str(newValue))

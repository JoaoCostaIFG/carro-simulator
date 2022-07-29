class Pedal:
    position: int = 0  # 0 -> not pressed. 100 -> fully pressed

    def changePos(self, newPos: int):
        self.position = newPos
        print("Changing Position of pedal to -> " + str(newPos))

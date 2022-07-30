#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config

from Pedal import Pedal
from HandBrake import HandBrake


class GuiWidget(Widget):
    def __init__(self, changeAccel, changeBrake, changeHandBrake, **kwargs):
        super().__init__(**kwargs)
        self.changeAccel = changeAccel
        self.changeBrake = changeBrake
        self.changeHandBrake = changeHandBrake

    def onChangeAccel(self):
        self.changeAccel(self.ids._accelSlider.value)

    def onChangeBrake(self):
        self.changeBrake(self.ids._brakeSlider.value)

    def onChangeHandBrake(self, switchValue):
        self.changeHandBrake(switchValue)

    pass


class GuiApp(App):
    accelerationPedal: Pedal = Pedal()
    brakePedal: Pedal = Pedal()
    handBrake: HandBrake = HandBrake()

    Config.set("graphics", "width", 800)
    Config.set("graphics", "height", 600)

    def build(self):
        return GuiWidget(
            self.accelerationPedal.changePos,
            self.brakePedal.changePos,
            self.handBrake.setActive,
        )


if __name__ == "__main__":
    GuiApp().run()

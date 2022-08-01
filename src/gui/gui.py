#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy_garden.speedmeter import SpeedMeter
from kivy.core.window import Window

from gui.Pedal import Pedal
from gui.HandBrake import HandBrake


class GuiWidget(Widget):
    def __init__(self, accelPedal : Pedal, brakePedal : Pedal, handBrake : HandBrake, **kwargs):
        super().__init__(**kwargs)
        self.accelPedal = accelPedal
        self.brakePedal = brakePedal
        self.handBrake = handBrake

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # TODO: CONNECT THE CLASSES WITH THE VALUE DISPLAYED IN THE UI
        if keycode[1] == 'w':
           self.brakePedal.incrementPos()
        elif keycode[1] == 's':
            self.brakePedal.decrementPos()
        elif keycode[1] == 'up':
            self.accelPedal.incrementPos()
        elif keycode[1] == 'down':
            self.accelPedal.decrementPos()
        elif keycode[1] == 'p':
            self.handBrake.toggleActive()
        elif keycode[1] == 'escape':
            print("EXITING...")


    def onChangeAccel(self, sliderValue):
        self.accelPedal.setPosition(sliderValue)

    def onChangeBrake(self, sliderValue):
        self.brakePedal.setPosition(sliderValue)

    def onChangeHandBrake(self, switchValue):
        self.handBrake.setActive(switchValue)

    def onChangeSpeed(self, speedValue):
        self.ids._speed.value = speedValue

    def onChangeRpm(self, rpmValue):
        self.ids._rpm.value = rpmValue / 1000


class GuiApp(App):
    def __init__(self) -> None:
        super().__init__()

        self.accelerationPedal: Pedal = Pedal()
        self.brakePedal: Pedal = Pedal()
        self.handBrake: HandBrake = HandBrake()

        Config.set("graphics", "width", 800)
        Config.set("graphics", "height", 600)

    def build(self):
        return GuiWidget(
            self.accelerationPedal,
            self.brakePedal,
            self.handBrake,
        )


if __name__ == "__main__":
    GuiApp().run()

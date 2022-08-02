#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy_garden.speedmeter import SpeedMeter
from kivy.core.window import Window
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget

from gui.carrowidget.CarroWidget import CarroWidget


class GuiWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def getAccelPos(self):
        return self.ids._accelSlider.value

    def getBrakePos(self):
        return self.ids._brakeSlider.value

    def getHandBrakeValue(self):
        return self.ids._parkingSwitch.active

    def setAccelPos(self, value):
        if (value >= 0 and value <= 100):
            self.ids._accelSlider.value = value

    def setBrakePos(self, value):
        if (value >= 0 and value <= 100):
            self.ids._brakeSlider.value = value

    def setHandBrakeValue(self, value):
        self.ids._parkingSwitch.active = value

    def onChangeSpeed(self, speedValue):
        self.ids._speed.value = speedValue
        normalizedSpeed = -1 if speedValue < 10 else ((250 - speedValue) / (240.) + 0.05) / 2

        if abs(self.ids._road.anim_delay - normalizedSpeed) > 0.05:
            self.ids._road.anim_delay = normalizedSpeed

    def onChangeRpm(self, rpmValue):
        self.ids._rpm.value = rpmValue / 1000

    def onChangeAccel(self, accelValue):
        self.ids._acceleration.accVal = round(accelValue, 2)

    def onChangeDecel(self, decelValue):
        self.ids._deceleration.decVal = round(decelValue, 2)

    def onChangeOperMode(self, newMode):
        self.ids._operMode.opMode = str(newMode)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            self.setBrakePos(self.getBrakePos() + 1)
        elif keycode[1] == 's':
            self.setBrakePos(self.getBrakePos() - 1)
        elif keycode[1] == 'up':
            self.setAccelPos(self.getAccelPos() + 1)
        elif keycode[1] == 'down':
            self.setAccelPos(self.getAccelPos() - 1)
        elif keycode[1] == 'p':
            self.setHandBrakeValue(not self.getHandBrakeValue())


class GuiApp(App):
    def __init__(self) -> None:
        super().__init__()

        Config.set("graphics", "width", 800)
        Config.set("graphics", "height", 800)

    def build(self):
        return GuiWidget()


if __name__ == "__main__":
    GuiApp().run()

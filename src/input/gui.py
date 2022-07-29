from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.config import Config

from Pedal import Pedal
from HandBrake import HandBrake

s = Slider(value_track=True, value_track_color=[1, 0, 0, 1])


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

    Config.set('graphics', 'width', 800)
    Config.set('graphics', 'height', 400)

    def build(self):
        return GuiWidget(self.accelerationPedal.changePos, self.brakePedal.changePos, self.handBrake.setActive)


if __name__ == '__main__':
    GuiApp().run()

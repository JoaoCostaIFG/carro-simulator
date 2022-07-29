from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.config import Config

from Pedal import Pedal

s = Slider(value_track=True, value_track_color=[1, 0, 0, 1])


class GuiWidget(Widget):
    def __init__(self, changeAccel, changeBrake, **kwargs):
        super().__init__(**kwargs)
        self.changeAccel = changeAccel
        self.changeBrake = changeBrake

    def onChangeAccel(self):
        self.changeAccel(self.ids._accelSlider.value)

    def onChangeBrake(self):
        self.changeBrake(self.ids._brakeSlider.value)

    pass


class GuiApp(App):
    accelerationPedal: Pedal = Pedal()
    brakePedal: Pedal = Pedal()

    Config.set('graphics', 'width', 800)
    Config.set('graphics', 'height', 400)

    def build(self):
        return GuiWidget(self.accelerationPedal.changePos, self.brakePedal.changePos)


if __name__ == '__main__':
    GuiApp().run()

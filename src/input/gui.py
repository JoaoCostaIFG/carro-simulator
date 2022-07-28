from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider

s = Slider(value_track=True, value_track_color=[1, 0, 0, 1])


class GuiWidget(Widget):
    pass


class GuiApp(App):
    def build(self):
        return GuiWidget()


if __name__ == '__main__':
    GuiApp().run()

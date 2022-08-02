import os

from kivy.app import App
from kivy3 import Scene, Renderer, PerspectiveCamera
from kivy3.loaders import OBJMTLLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock

# Resources pathes
_this_path = os.path.dirname(os.path.realpath(__file__))
shader_file = os.path.join(_this_path, "./new.glsl")
obj_file = os.path.join(_this_path, "./lowpoly_car.obj")
mtl_file = os.path.join(_this_path, "./lowpoly_car.mtl")


class CarroWidget(Renderer):
    def __init__(self, **kwargs):
        super().__init__(shader_file=shader_file, **kwargs)

        scene = Scene()
        camera = PerspectiveCamera(60, 1, 1, 50)
        loader = OBJMTLLoader()
        obj = loader.load(obj_file, mtl_file)

        scene.add(*obj.children)
        for obj in scene.children:
            obj.pos.z = -3
            obj.pos.y = -0.5

        self.render(scene, camera)
        self.car = scene.children

        self.bind(size=self._adjust_aspect)
        Clock.schedule_interval(self._rotate_obj, 1. / 20)

    def _rotate_obj(self, dt):
        for peca in self.car:
            peca.rot.y += 2

    def _adjust_aspect(self, inst, val):
        rsize = self.size
        aspect = rsize[0] / float(rsize[1])
        self.camera.aspect = aspect


if __name__ == '__main__':
    class MainApp(App):
        def build(self):
            root = FloatLayout()
            self.carro = CarroWidget()
            root.add_widget(self.carro)
            return root

    MainApp().run()

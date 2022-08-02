"""
The MIT License (MIT)

Copyright (c) 2014 Niko Skrypnik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import os
from kivy.app import App
from kivy3 import Scene, Renderer, PerspectiveCamera
from kivy3.loaders import OBJMTLLoader, OBJLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

# Resources pathes
_this_path = os.path.dirname(os.path.realpath(__file__))
shader_file = os.path.join(_this_path, "./new.glsl")
obj_file = os.path.join(_this_path, "./lowpoly_car.obj")
mtl_file = os.path.join(_this_path, "./lowpoly_car.mtl")


class MainApp(App):

    def build(self):
        root = FloatLayout()
        self.renderer = Renderer(shader_file=shader_file)
        scene = Scene()
        camera = PerspectiveCamera(60, 1, 1, 1000)
        loader = OBJMTLLoader()
        obj = loader.load(obj_file, mtl_file)
        #  loader = OBJLoader()
        #  obj = loader.load(obj_file)

        scene.add(*obj.children)
        for obj in scene.children:
            obj.pos.z = -3
            obj.pos.y = -0.5

        self.renderer.render(scene, camera)
        self.car = scene.children

        root.add_widget(self.renderer)
        self.renderer.bind(size=self._adjust_aspect)
        Clock.schedule_interval(self._rotate_obj, 1. / 20)
        return root

    def _rotate_obj(self, dt):
        for peca in self.car:
            peca.rot.y += 2

    def _adjust_aspect(self, inst, val):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect


if __name__ == '__main__':
    MainApp().run()

import glfw
import numpy as np

class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.theta = -3*(np.pi/4)
        self.eye = [1, 1, 1.5]
        self.at = [0, 0, 0.1]
        self.up = [0,0,1]
        self.lock = True

    def on_key(self, window, key, scancode, action, mods):

        if action != glfw.PRESS and action != glfw.REPEAT:
            return

        if key == glfw.KEY_P:
            self.fillPolygon = not self.fillPolygon

        elif key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)

        elif key == glfw.KEY_W:

            self.eye += (self.at - self.eye) * 0.05
            self.at += (self.at - self.eye) * 0.05
        
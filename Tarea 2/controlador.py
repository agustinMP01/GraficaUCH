import numpy as np
import glfw

class Controller:
    def __init__(self):

        self.theta = np.pi
        self.eye = [0, 0, 0.1]
        self.at = [0, 1, 0.1]
        self.up = [0, 0, 1]

    def on_key(self,window, key, scancode, action, mods):
        
        if not (action == glfw.PRESS):
            return

        elif key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)
    
        elif key == glfw.KEY_W:
            self.eye += (self.at - self.eye) * 0.05
            self.at += (self.at - self.eye) * 0.05


        else:
            print('Unknown key')    
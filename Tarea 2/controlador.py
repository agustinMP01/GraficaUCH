import numpy as np
import glfw

class Controller:
    def __init__(self):

        self.theta = -np.pi/2
        self.eye = [-1*np.cos(self.theta),1*np.sin(self.theta), 0.1] #Donde estoy
        self.at = [0, 0, 0] #Hacia donde miro
        self.up = [0, 0, 1] #No se toca, indica normal

    def on_key(self, window, key, scancode, action, mods):

        if action != glfw.PRESS and action != glfw.REPEAT:
            return

        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)
            
        else:
            print('Unknown key')

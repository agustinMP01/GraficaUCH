import numpy as np
import glfw

class Controller:
    def __init__(self):

        self.r = 1
        self.theta = -np.pi/2
        self.eye = [-self.r*np.cos(self.theta),self.r*np.sin(self.theta), 0.1] #Donde estoy
        self.at = [0, 0, 0] #Hacia donde miro
        self.up = [0, 0, 1] #No se toca, indica normal
        self.current = 0

        self.lock = True

    def on_key(self, window, key, scancode, action, mods):

        if action != glfw.PRESS and action != glfw.REPEAT:
            return

        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)

        if key == glfw.KEY_1:
            return
        if key == glfw.KEY_2:
            return
        if key == glfw.KEY_3:
            return            
        if key == glfw.KEY_4:
            return
            
        #CAMARA LIBRE EN CILINDRICA    
        if key == glfw.KEY_5:
            self.theta = -np.pi/2
            self.eye = [-1*np.cos(self.theta),1*np.sin(self.theta), 0.1] #Donde estoy
            self.at = [0, 0, 0] #Hacia donde miro
            self.up = [0, 0, 1] #No se toca, indica normal    
            self.lock = False

        if key == glfw.KEY_1:
            self.lock = True   

        if key == glfw.KEY_2:
            self.lock = True  

        if key == glfw.KEY_3:
            self.lock = True  

        if key == glfw.KEY_4:
            self.lock = True  
                                                 
        #CAMBIAR EDIFICIOS
        if key == glfw.KEY_E:
            self.current = 0

        if key == glfw.KEY_W:
            self.current = 1

        if key == glfw.KEY_B:
            self.current = 2    

        else:
            print('Unknown key')

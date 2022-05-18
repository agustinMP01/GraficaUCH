import glfw
from OpenGL.GL import *
import sys
 
import grafica.transformations as tr
import grafica.easy_shaders as es
import grafica.scene_graph as sg
import grafica.lighting_shaders as ls
from modelo import *
from controlador import *
import numpy as np

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 1920
    height = 1080

    window = glfw.create_window(width, height, "Flappy Bird", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    #CONTROLLER -> ON_KEY
    controller = Controller()
    glfw.set_key_callback(window,controller.on_key)

    ''' PIPELINE '''

    # Creating shader programs for textures and for colors
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    lightShaderProgram = ls.SimpleGouraudShaderProgram()  # Spoiler de luces

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    '''MODELOS '''
    skybox = Skybox(textureShaderProgram)

    '''CAMARA Y PROYECCION'''
    projection = tr.perspective(60, float(width)/float(height), 0.1, 100)

    '''MODELO-CONTROLADOR'''

    '''CICLO WHILE'''
    t0 = glfw.get_time()
    camera_theta = -3 * np.pi / 4

    while not glfw.window_should_close(window):
        ti = glfw.get_time()
        dt = ti-t0
        t0 = ti


        #Eventos
        glfw.poll_events()

        #Limpiar pantalla       
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #MOVIMIENTO
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            controller.theta += 2 * dt

        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            controller.theta -= 2 * dt

        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            controller.eye += (controller.at - controller.eye) * dt
            controller.at += (controller.at - controller.eye) * dt

        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            controller.eye -= (controller.at - controller.eye) * dt
            controller.at -= (controller.at - controller.eye) * dt

        at_x = controller.eye[0] + np.cos(controller.theta)
        at_y = controller.eye[1] + np.sin(controller.theta)
        controller.at = np.array([at_x, at_y, controller.at[2]])

        view = tr.lookAt(controller.eye, controller.at, controller.up)

        #Updates

        #Logica

        #Draws
        skybox.draw(textureShaderProgram,projection,view)

        glfw.swap_buffers(window)

    #Cerramos
    glfw.terminate()
    sys.exit()    

import glfw
from OpenGL.GL import *
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.scene_graph as sg
import grafica.lighting_shaders as ls
from grafica.assets_path import getAssetPath
import off_obj_reader as obj
from controlador import *
import modelost


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 1920
    height = 1080

    window = glfw.create_window(width, height, "Viewer", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    controller = Controller()
    glfw.set_key_callback(window, controller.on_key)

    # Creating shader programs for textures and for colors
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    lightShaderProgram = ls.SimpleGouraudShaderProgram()  # Spoiler de luces
    textureLightShaderProgram = ls.SimpleTextureGouraudShaderProgram()

    #Color de fondo*
    glClearColor(0, 0.7, 0.5, 0.8)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory

    floor = modelost.create_floor(textureShaderProgram)
    empire = modelost.empire_state(textureLightShaderProgram)
    willis = modelost.willis_tower(textureLightShaderProgram)

    torres = [empire,willis]

    #projection
    projection = tr.perspective(60, float(width)/float(height), 0.1, 100)

    t0 = glfw.get_time()

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    t1 = glfw.get_time()
    t1 = glfw.get_time()

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        # Filling or not the shapes depending on the controller state
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)


        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

   #####################################################


   #Flechas controlan la camara, a los lados gira y hacia arriba/abajo sube y baja. Con Z se hace zoom, con X se aleja

        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
            controller.eye[2] += 2*dt

        if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
            controller.eye[2] -= 2*dt

        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
            controller.theta += 2*dt
            controller.eye = [-controller.r*np.cos(controller.theta),controller.r*np.sin(controller.theta), controller.eye[2]]

        if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
            controller.theta -= 2*dt
            controller.eye = [-controller.r*np.cos(controller.theta),controller.r*np.sin(controller.theta), controller.eye[2]]

        if controller.eye[2] <= 0.1:
            controller.eye[2] = 0.1

        if glfw.get_key(window, glfw.KEY_Z) == glfw.PRESS:
            controller.r -= 2*dt
            controller.eye = [-controller.r*np.cos(controller.theta),controller.r*np.sin(controller.theta), controller.eye[2]]
        if glfw.get_key(window, glfw.KEY_X) == glfw.PRESS:
            controller.r += 2*dt
            controller.eye = [-controller.r*np.cos(controller.theta),controller.r*np.sin(controller.theta), controller.eye[2]]            
    #####################################################        

        controller.at = np.array([0, 0, controller.at[2]])

        view = tr.lookAt(controller.eye, controller.at, controller.up)

###########################################################################

        #W: Willis
        #E: Empire State

        current = torres[controller.current]



        # Drawing
        glUseProgram(textureShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)

        sg.drawSceneGraphNode(floor, textureShaderProgram, "model")

        #LUZ? Se va a negro
        glUseProgram(textureLightShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        # textureLightShaderProgram.set_light_attributes()
        
        sg.drawSceneGraphNode(current, textureLightShaderProgram, "model")


        glfw.swap_buffers(window)

    glfw.terminate()

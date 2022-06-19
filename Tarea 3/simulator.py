# coding=utf-8
"""
Se agrega la torre Eiffel al medio, para mostrarles cómo funcionan
las mallas y que podemos tenerlas almacenadas en objetos
.OBJ
Estos se pueden generar en programas como Blender, Maya, Rhino o
SketchUp. También es común descargarlos de páginas como:
https://3dwarehouse.sketchup.com/search/?q=eiffel%20tower
https://quixel.com/megascans/home?category=3D%20asset&category=building
Etc. Lo ideal es googlear por .OBJ o .OFF 3D models
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
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
import modelos
import controller
import auxs as ax

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 1920  
    height = 1080

    window = glfw.create_window(width, height, "Dice", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events

    control = controller.Controller()

    glfw.set_key_callback(window, control.on_key)

    # Creating shader programs for textures and for colors
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    lightShaderProgram = ls.SimplePhongShaderProgram()  # Spoiler de luces
    textureLightShaderProgram = ls.SimpleTexturePhongShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory

    floor = modelos.create_floor(textureShaderProgram)
    mountain = modelos.create_mountain(textureLightShaderProgram)
    barco = modelos.Boat(textureLightShaderProgram)
    x =0
    y=0
    coordinates = ax.txtToList(sys.argv[1])
    print(coordinates)

    # View and projection
    projection = tr.perspective(60, float(width)/float(height), 0.1, 100)

    t0 = glfw.get_time()
    camera_theta = -3 * np.pi / 4

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
        if (control.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            control.eye += (control.at - control.eye) * dt
            control.at += (control.at - control.eye) * dt

        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            control.eye -= (control.at - control.eye) * dt
            control.at -= (control.at - control.eye) * dt

        if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
            control.eye[2] += 2*dt
            control.at[2] += 2*dt

        if glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
            control.eye[2] -= 2*dt
            control.at[2] -= 2*dt

        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
            control.at[2] += 2*dt

        if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
            control.at[2] -= 2*dt            

        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
            control.theta += 2 * dt

        if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
            control.theta -= 2 * dt

        #Testear mov
        if glfw.get_key(window, glfw.KEY_J) == glfw.PRESS:
            y += dt

        if glfw.get_key(window, glfw.KEY_L) == glfw.PRESS:
            y -= dt
        ##################################################

        at_x = control.eye[0] + np.cos(control.theta)
        at_y = control.eye[1] + np.sin(control.theta)
        control.at = np.array([at_x, at_y, control.at[2]])

        view = tr.lookAt(control.eye, control.at, control.up)

###########################################################################

        #Dibujar piso
        glUseProgram(textureShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)

        sg.drawSceneGraphNode(floor, textureShaderProgram, "model")

        #Dibujar montaña
        glUseProgram(textureLightShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)

        #Setea luces
        textureLightShaderProgram.set_light_attributes()

        sg.drawSceneGraphNode(mountain, textureLightShaderProgram, "model")

        #Actualizar posicion del barco
        barco.model.transform = tr.translate(x,y,0) #Ahora, x e y deben ser dados por la spline catmull rom

        barco.draw(textureLightShaderProgram, projection, view)


        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()


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

    #Inicio ventana con glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    #Altura y ancho
    width = 1920
    height = 1080

    window = glfw.create_window(width, height, "Viewer", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    #Setear controller y recibir teclas
    controller = Controller()
    glfw.set_key_callback(window, controller.on_key)

    #Shaders a utilizar
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram() 
    lightShaderProgram = ls.SimpleGouraudShaderProgram()  
    textureLightShaderProgram = ls.SimpleTextureGouraudShaderProgram()
    SimpleShader = es.SimpleModelViewProjectionShaderProgram()

    #Color de fondo*
    glClearColor(0, 0.7, 0.5, 0.8)

    #Checkear profundidad 3d
    glEnable(GL_DEPTH_TEST)

    #Creamos los modelos

    floor_willis = modelost.create_floor(textureShaderProgram, "maps_willis.jpg")
    floor_empire = modelost.create_floor(textureShaderProgram, "maps_empire.jpg")
    floor_burj = modelost.create_floor(textureShaderProgram, "maps_burj.jpg")

    empire = modelost.empire_state(textureLightShaderProgram)
    willis = modelost.willis_tower(textureLightShaderProgram)
    burj = modelost.burj(textureLightShaderProgram)
    sphere1 = modelost.color_sphere1(SimpleShader)
    sphere2 = modelost.color_sphere2(SimpleShader)

    #Lista auxiliar para cambiar facilmente entre modelos
    torres = [empire, willis, burj]
    floors = [floor_empire, floor_willis,floor_burj]
    floors_current = floors[0]

    #projection
    pers = tr.perspective(60, float(width)/float(height), 0.1, 100) 
    ortho = tr.ortho(-1,1,-1.5,0.75,0.1,100)

    #Lista auxiliar para cambiar facilmente entre camaras
    cameras = [pers, ortho]
    cam_current = cameras[0] #<- Camara utilizada actualmente, default = pers

    #Inicializamos nuestro dt
    t0 = glfw.get_time()

    #Intercambiar buffers
    glfw.swap_interval(0)

    while not glfw.window_should_close(window):

        #Revisar inputs
        glfw.poll_events()

        #Calcular dt
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        # Filling or not the shapes depending on the controller state
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)


        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

   #####################################################
   #Controlador en tiempo real para actualizar camaras y movimiento
   # 1<- camara pers 1. 
   # 2<- camara pers 2. 
   # 3<- camara ortho 1. 
   # 4<- camara ortho 2
   # 5<- camara libre con vista perspectiva y coordenadas cilindricas.
        if glfw.get_key(window, glfw.KEY_1) == glfw.PRESS:
            cam_current = cameras[0]
            controller.lock = True
            controller.theta = 0
            controller.eye = [1, 1, 0.1]   
            controller.at = [0, 0, 0.5]          

        if glfw.get_key(window, glfw.KEY_2) == glfw.PRESS:
            cam_current = cameras[0]
            controller.lock = True
            controller.theta = 0
            controller.eye = [-1, -1, 2]   
            controller.at = [0, 0, 0.5]   

        if glfw.get_key(window, glfw.KEY_3) == glfw.PRESS:
            cam_current = cameras[1]
            controller.lock = True
            controller.theta = 0
            controller.eye = [-1, -1, 1.5]   
            controller.at = [1, 1, 1]          

        if glfw.get_key(window, glfw.KEY_4) == glfw.PRESS:
            cam_current = cameras[1]
            controller.lock = True
            controller.theta = 0
            controller.eye = [1, 1, 1.5]   
            controller.at = [1, 1, 1]   

        if glfw.get_key(window, glfw.KEY_5) == glfw.PRESS:
            cam_current = cameras[0]
            controller.theta = -np.pi/2
            controller.eye = [-1*np.cos(controller.theta),1*np.sin(controller.theta), 0.1] #Donde estoy
            controller.at = [0, 0, 0] #Hacia donde miro
            controller.up = [0, 0, 1] #Indica normal    
            controller.lock = False


        #Controlador para la camara libre:
        #Flecha arriba <- la camara se eleva en el eje z
        #Flecha abajo <- la camara desciende en el eje z 
        #Flecha izq <- se aumenta el angulo theta, la camara rota en sentido horario
        #flecha der <- disminuye el angulo theta, la camara rota en sentido antihorario
        #Z <- disminuye el radio, la camara se acerca al modelo
        #X <- aumenta el radio, la camara se aleja del modelo
        if not controller.lock:

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

            #Limites para el radio, de esta forma no tenemos radio negativo que invierte los controles Z y X.
            #Evita ademas tener una camara infinitamente lejos del modelo
            if controller.r <= 0:
                controller.r = 0

            if controller.r >=5:
                controller.r = 5        

    #####################################################        

        #Define el vector at para la camara
        controller.at = np.array([0, 0, controller.at[2]])

        #Define el vector view
        view = tr.lookAt(controller.eye, controller.at, controller.up)

###########################################################################

        #Lista auxiliar que permite dibujar la torre seleccionada en un mismo bloque de codigo
        #W: Willis
        #E: Empire State
        #B: Burj Al Arab

        current = torres[controller.current]
        floor_current = floors[controller.current]

        # Dibujamos el piso, figura plana en 2d
        glUseProgram(textureShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, cam_current)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)

        sg.drawSceneGraphNode(floor_current, textureShaderProgram, "model")

        
        glUseProgram(SimpleShader.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(SimpleShader.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(SimpleShader.shaderProgram, "projection"), 1, GL_TRUE, cam_current)

        sg.drawSceneGraphNode(sphere1, SimpleShader, "model")
        sg.drawSceneGraphNode(sphere2, SimpleShader, "model")

        #Dibujamos los modelos, figuras en 3d
        glUseProgram(textureLightShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, cam_current)

        #Luces, cambia segun el edificio actual. Mayoria de valores se mantienen constantes, notorio que
        #Posicion <- cambia intentando imitar la posicion actual de la luz segun las sombras basandose en Maps
        #Color <- Willis y Empire tienen el mismo color pues estan en el mismo pais/ambiente. 
        #   Burj cambia a un tono mas amarillento pero no tan notorio (ver codigo en grafica<lighting_shader<set_light_attributes)
        #Factores Ka, Kd, Ks <- Cambian ligeramente para simular las ventanas de los edificos
        textureLightShaderProgram.set_light_attributes(controller.current)

        #Dibuja el edificio actual.
        sg.drawSceneGraphNode(current, textureLightShaderProgram, "model")

        #Cambiamos buffers
        glfw.swap_buffers(window)

    glfw.terminate()

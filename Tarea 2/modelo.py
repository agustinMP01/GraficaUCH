import glfw
from OpenGL.GL import * 
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.scene_graph as sg
from grafica.assets_path import getAssetPath
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Skybox(object):

    def __init__(self,pipeline):
        shapeSky = bs.createTextureCube('paisaje.jpg')
        gpuSky = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpuSky)
        gpuSky.fillBuffers(shapeSky.vertices, shapeSky.indices, GL_STATIC_DRAW)
        gpuSky.texture = es.textureSimpleSetup(
         getAssetPath("paisaje.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
        skybox = sg.SceneGraphNode("skybox")
        skybox.transform = tr.matmul([tr.translate(0, 0, 0), tr.uniformScale(1)])
        skybox.childs += [gpuSky]

        self.model = skybox

    def draw(self,pipeline,projection,view):
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    
        sg.drawSceneGraphNode(self.model, pipeline, "model")

class Flappy(object):

    def __init__(self,pipeline):
        shapeFlappy = bs.createTextureCube("red.jpg")
        gpuFlappy = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpuFlappy)
        gpuFlappy.fillBuffers(shapeFlappy.vertices, shapeFlappy.indices, GL_STATIC_DRAW)
        gpuFlappy.texture = es.textureSimpleSetup(
            getAssetPath("red.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

        flappy = sg.SceneGraphNode("flappy")
        flappy.transform = tr.uniformScale(1)
        flappy.childs += [gpuFlappy]    

        self.model = gpuFlappy
        self.pos = [0,0,0]
        self.vel_y = 0
        self.alive = True


    def move_up(self):
        self.vel_y = 1

    def draw(self,pipeline,projection,view):
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE,tr.matmul([tr.translate(self.pos[0],self.pos[1],self.pos[2]),tr.uniformScale(1)]))

        pipeline.drawCall(self.model)

    def update(self,dt):
        if self.alive:
        #Gravedad y velocidad terminal que afectan a flappy
            grav = -2
            terminal_vel = 2

            if not self.alive:
                self.pos[2] = 0.25

            while self.pos[2] > 0.99:
                self.pos[2] = 0.99

        #Caida libre en cada update
            self.pos[2] += self.vel_y*dt

        #Limite para velocidad al caer
            if self.vel_y > -terminal_vel:
                self.vel_y += grav*dt

        else:
            return

class Floor(object):
    
    def __init__(self,pipeline):
        shapeFloor = bs.createTextureQuad(8, 8)
        gpuFloor = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpuFloor)
        gpuFloor.texture = es.textureSimpleSetup(
        getAssetPath("pholder.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
        gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)

        floor = sg.SceneGraphNode("floor")
        floor.transform = tr.matmul([tr.translate(0, 0, 0),tr.scale(2, 2, 1)])
        floor.childs += [gpuFloor]

        self.model = gpuFloor

    def draw(self,pipeline,projection,view):
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        pipeline.drawCall(self.model)

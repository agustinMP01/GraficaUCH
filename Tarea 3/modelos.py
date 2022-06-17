from OpenGL.GL import *
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.scene_graph as sg
from grafica.assets_path import getAssetPath




def create_floor(pipeline):
    shapeFloor = bs.createTextureQuad(2, 2)
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.texture = es.textureSimpleSetup(
        getAssetPath("pholder.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)

    floor = sg.SceneGraphNode("floor")
    floor.transform = tr.uniformScale(2)
    floor.childs += [gpuFloor]

    return floor

def create_mountain(pipeline):
    shapeBox = bs.createTextureNormalsCube("pholder.jpg")
    gpuBox = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBox)
    gpuBox.texture= es.textureSimpleSetup(
        getAssetPath("pholder.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR) 
    gpuBox.fillBuffers(shapeBox.vertices, shapeBox.indices, GL_STATIC_DRAW)

    box = sg.SceneGraphNode("box")
    box.transform = tr.translate(0,0,0.5)
    box.childs += [gpuBox]

    return box

class Boat:
    def __init__(self,pipeline):

        #Atributos
        self.pos = [0,0,0] #Posicion x,y,z
        self.vel = 0       #Velocidad para moverse
        self.dir = 0       #Direccion, donde apunta el frente
        self.movement = tr.translate(self.pos[0],self.pos[1],0)

        #Modelo en si
        shapeBox = bs.createTextureNormalsCube("pholder.jpg")
        gpuBox = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpuBox)
        gpuBox.texture= es.textureSimpleSetup(
            getAssetPath("pholder.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR) 
        gpuBox.fillBuffers(shapeBox.vertices, shapeBox.indices, GL_STATIC_DRAW)

        #Lados
        lado1 = sg.SceneGraphNode("lado1")
        lado1.transform = tr.matmul([tr.scale(0.2,0.01,0.1),tr.translate(0,5,0.5)])
        lado1.childs += [gpuBox]

        lado2 = sg.SceneGraphNode("lado2")
        lado2.transform = tr.matmul([tr.scale(0.2,0.01,0.1),tr.translate(0,-5,0.5)])
        lado2.childs += [gpuBox]

        lados = sg.SceneGraphNode("lados")
        lados.transform = tr.identity()
        lados.childs += [lado1, lado2]

        #frentes
        frente1 = sg.SceneGraphNode("frente1")
        frente1.transform = tr.matmul([tr.scale(0.01,0.1,0.1),tr.translate(10,0,0.5)])
        frente1.childs += [gpuBox] 

        frente2 = sg.SceneGraphNode("frente2")
        frente2.transform = tr.matmul([tr.scale(0.01,0.1,0.1),tr.translate(-10,0,0.5)])
        frente2.childs += [gpuBox] 

        frentes = sg.SceneGraphNode("frente")
        frentes.transform = tr.identity()
        frentes.childs += [frente1, frente2]

        #Piso
        piso = sg.SceneGraphNode("piso")
        piso.transform = tr.matmul([tr.scale(0.2,0.1,0.01),tr.translate(0,0,0.5)])
        piso.childs += [gpuBox]

        #Barco
        self.model = sg.SceneGraphNode("barco")
        self.model.transform = tr.translate(self.pos[0],self.pos[1],0)
        self.model.childs += [lados, piso, frentes]


    def draw(self, pipeline, projection, view):

        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        sg.drawSceneGraphNode(self.model, pipeline, "model")






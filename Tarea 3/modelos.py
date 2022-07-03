from random import randint
from OpenGL.GL import *
import sys
import os.path


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.scene_graph as sg
from grafica.assets_path import getAssetPath
from grafica.mathlib import _normal_3_points as _normal3
import numpy as np


def create_floor(pipeline):
    shapeFloor = bs.createRainbowQuad()
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)

    floor = sg.SceneGraphNode("floor")
    floor.transform = tr.uniformScale(1)
    floor.childs += [gpuFloor]

    return floor

def create_mountain(pipeline):
    '''
    Crea una montaña 1x1 subdividiendo en 9 cuadrados con 3 opciones al azar
    '''

    #Verde
    shapeGreen = bs.createColorNormalsCube(0,1,0)
    gpuGreen = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuGreen)
    gpuGreen.fillBuffers(shapeGreen.vertices, shapeGreen.indices, GL_STATIC_DRAW)

    green = sg.SceneGraphNode("green")
    green.transform = tr.translate(0,0,0.5)
    green.childs += [gpuGreen]

    #Cafe
    shapeBrown = bs.createColorNormalsCube(0.07,0.03,0)
    gpuBrown = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBrown)
    gpuBrown.fillBuffers(shapeBrown.vertices, shapeBrown.indices, GL_STATIC_DRAW)

    brown = sg.SceneGraphNode("brown")
    brown.transform = tr.translate(0,0,0.5)
    brown.childs += [gpuBrown]

    #Blanco
    shapeWhite = bs.createColorNormalsCube(0.925,0.925,0.925)
    gpuWhite = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuWhite)
    gpuWhite.fillBuffers(shapeWhite.vertices, shapeWhite.indices, GL_STATIC_DRAW)

    white = sg.SceneGraphNode("white")
    white.transform = tr.translate(0,0,0.5)
    white.childs += [gpuWhite]

    #Modulo 1
    m1_bottom = sg.SceneGraphNode("m1_bottom")
    m1_bottom.transform = tr.scale(0.33,0.33,0.5)
    m1_bottom.childs += [green]

    m1_mid = sg.SceneGraphNode("m1_mid")
    m1_mid.transform = tr.matmul([tr.translate(0,0,0.5),tr.scale(0.33,0.33,0.3)])
    m1_mid.childs += [brown]

    m1_top = sg.SceneGraphNode("m1_top")
    m1_top.transform = tr.matmul([tr.translate(0,0,0.8),tr.scale(0.33,0.33,0.2)])
    m1_top.childs += [white]

    m1 = sg.SceneGraphNode("m1")
    m1.childs += [m1_bottom, m1_mid, m1_top]

    #Modulo 2
    m2_bottom = sg.SceneGraphNode("m2_bottom")
    m2_bottom.transform = tr.scale(0.33,0.33,0.5)
    m2_bottom.childs += [green]

    m2_mid = sg.SceneGraphNode("m2_mid")
    m2_mid.transform = tr.matmul([tr.translate(0,0,0.5),tr.scale(0.33,0.33,0.3)])
    m2_mid.childs += [brown]

    m2 = sg.SceneGraphNode("m2")
    m2.childs += [m2_bottom, m2_mid]

    #Modulo 3
    m3_bottom = sg.SceneGraphNode("m3_bottom")
    m3_bottom.transform = tr.scale(0.33,0.33,0.5)
    m3_bottom.childs += [green]

    m3 = sg.SceneGraphNode("m3")
    m3.childs += [m3_bottom]





    #montaña
    mountain = sg.SceneGraphNode("mountain")
    mountain.transform = tr.identity()

    #Transforms
    translates = [(0.33,0.33,0),(-0.33,-0.33,0),(0,0,0),
                  (-0.33,0.33,0),(0.33,-0.33,0),(0.33,0,0),
                  (-0.33,0,0), (0,0.33,0),(0,-0.33,0)]

    #Modules
    modules = [m1, m2, m3]


    #Randomizer :D
    for i in range(len(translates)):
        name = str("module" + str(i))

        random_tr = (randint(0,8))%len(translates)
        random_mod = randint(0,2)
        translate = translates[random_tr]
        translates.pop(random_tr)
        module = sg.SceneGraphNode(name)
        module.transform = tr.translate(translate[0],translate[1],translate[2])
        module.childs = modules[random_mod].childs

        mountain.childs += [module]

    return mountain

class Boat:
    def __init__(self,pipeline):

        #Atributos
        self.ang = 0
        self.x = 0
        self.y = 0

        #Modelo en si
        shapeBox = bs.createTextureNormalsCube("wood.jpg")
        gpuBox = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpuBox)
        gpuBox.texture= es.textureSimpleSetup(
            getAssetPath("wood.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR) 
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
        self.model.transform = tr.identity()
        self.model.childs += [lados, piso, frentes]


    def draw(self, pipeline, projection, view):

        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        sg.drawSceneGraphNode(self.model, pipeline, "model")

    def update(self, points, current, ang):

        self.ang = ang[(current)%len(ang)]
        n = len(points)
        self.model.transform = tr.matmul([tr.translate(points[(2*current)%n],points[(2*current+1)%n],0),tr.rotationZ(self.ang)])    
        self.x = points[(2*current)%n]
        self.y = points[(2*current+1)%n]


def CatmullRom(points,pipeline):
    shapeSpline, mov, ang = bs.CatmullRomRGB(points,100,1,0,0)
    gpuSpline = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuSpline)
    gpuSpline.fillBuffers(shapeSpline.vertices, shapeSpline.indices, GL_STATIC_DRAW)

    spline = sg.SceneGraphNode("spline")
    spline.transform = tr.identity()
    spline.childs += [gpuSpline]

    return spline, mov, ang
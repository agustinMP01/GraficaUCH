from poplib import POP3
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
from grafica.assets_path import getAssetPath


def create_floor(pipeline, texture):
    shapeFloor = bs.createTextureQuad(1, 1)
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.texture = es.textureSimpleSetup(
        getAssetPath(texture), GL_CLAMP_TO_BORDER, GL_CLAMP_TO_BORDER, GL_LINEAR, GL_LINEAR)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)

    floor = sg.SceneGraphNode("floor")
    floor.transform = tr.uniformScale(2)
    floor.childs += [gpuFloor]

    return floor

def empire_state(pipeline):
    #Caja
    shapeBox = bs.createTextureNormalsCube("building.jpg")
    gpuBox = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBox)
    gpuBox.texture = es.textureSimpleSetup(
        getAssetPath("building.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuBox.fillBuffers(shapeBox.vertices, shapeBox.indices, GL_STATIC_DRAW)

    #base
    base= sg.SceneGraphNode("base")
    base.transform = tr.matmul([tr.scale(1.1,0.5,0.306),tr.translate(0,0,0.5)])
    base.childs += [gpuBox] 

    #main
    main = sg.SceneGraphNode("main")
    main.transform = tr.matmul([tr.scale(0.35,0.25,3.239),tr.translate(0,0,0.5)])
    main.childs += [gpuBox]

    #floor 1
    floor1_1 = sg.SceneGraphNode("floor1_1") #cacho izq
    floor1_1.transform = tr.matmul([tr.scale(0.2,0.5,0.459),tr.translate(-1.25,0,0)])
    floor1_1.childs += [gpuBox]

    floor1_2 = sg.SceneGraphNode("floor1_2") #cacho der
    floor1_2.transform = tr.matmul([tr.scale(0.2,0.5,0.459),tr.translate(1.25,0,0)])
    floor1_2.childs += [gpuBox]

    floor1_3 = sg.SceneGraphNode("floor1_3") #cacho grande izq
    floor1_3.transform = tr.matmul([tr.scale(0.2,0.3,0.359),tr.translate(-1.5,0,-0.278)])
    floor1_3.childs += [gpuBox]

    floor1_4 = sg.SceneGraphNode("floor1_4") #cacho grande der
    floor1_4.transform = tr.matmul([tr.scale(0.2,0.3,0.359),tr.translate(1.5,0,-0.278)])
    floor1_4.childs += [gpuBox]    

    floor1 = sg.SceneGraphNode("floor1") 
    floor1.transform = tr.translate(0,0,0.45)
    floor1.childs += [floor1_1,floor1_2, floor1_3, floor1_4]

    #floor 2
    floor2 = sg.SceneGraphNode("floor2") #Atraviesa todo main y le salen cachos
    floor2.transform = tr.matmul([tr.scale(0.625,0.375,0.559),tr.translate(0,0,1)])
    floor2.childs += [gpuBox]

    #floor 3
    floor3_1 = sg.SceneGraphNode("floor3_1") #cacho izq
    floor3_1.transform = tr.matmul([tr.scale(0.187,0.362,2.49),tr.translate(-1,0,0.5)])
    floor3_1.childs += [gpuBox]

    floor3_2 = sg.SceneGraphNode("floor3_2") #cacho izq
    floor3_2.transform = tr.matmul([tr.scale(0.187,0.362,2.49),tr.translate(1,0,0.5)])
    floor3_2.childs += [gpuBox]

    floor3 = sg.SceneGraphNode("floor3")
    floor3.transform = tr.identity()
    floor3.childs += [floor3_1, floor3_2]

    #floor 4
    floor4_1 = sg.SceneGraphNode("floor4_1") #cacho izq
    floor4_1.transform = tr.matmul([tr.scale(0.162,0.337,2.95),tr.translate(-1,0,0.5)])
    floor4_1.childs += [gpuBox]

    floor4_2 = sg.SceneGraphNode("floor4_2") #cacho izq
    floor4_2.transform = tr.matmul([tr.scale(0.162,0.337,2.95),tr.translate(1,0,0.5)])
    floor4_2.childs += [gpuBox]

    floor4 = sg.SceneGraphNode("floor4")
    floor4.transform = tr.identity()
    floor4.childs += [floor4_1, floor4_2]

    #Empire State
    empire = sg.SceneGraphNode("empire")
    empire.transform = tr.uniformScale(0.5)
    empire.childs += [base, main, floor1, floor2, floor3, floor4]

    return empire

def willis_tower(pipeline):
    #Caja
    shapeBox = bs.createTextureNormalsCube("willis2.jpg")
    gpuBox = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBox)
    gpuBox.texture = es.textureSimpleSetup(
        getAssetPath("willis2.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuBox.fillBuffers(shapeBox.vertices, shapeBox.indices, GL_STATIC_DRAW)

    #torre 50
    torre50_1 = sg.SceneGraphNode("torre50_1")
    torre50_1.transform = tr.matmul([tr.scale(0.3,0.3,1.5),tr.translate(1,-1,0.5)])
    torre50_1.childs += [gpuBox]


    torre50_2 = sg.SceneGraphNode("torre50_2")
    torre50_2.transform = tr.matmul([tr.scale(0.3,0.3,1.5),tr.translate(-1,1,0.5)])
    torre50_2.childs += [gpuBox]

    torre50 = sg.SceneGraphNode("torre50")
    torre50.transform = tr.identity()
    torre50.childs += [torre50_1, torre50_2]

    #torre 66
    torre66_1 = sg.SceneGraphNode("torre66_1")
    torre66_1.transform = tr.matmul([tr.scale(0.3,0.3,1.89),tr.translate(-1,-1,0.5)])
    torre66_1.childs += [gpuBox]


    torre66_2 = sg.SceneGraphNode("torre66_2")
    torre66_2.transform = tr.matmul([tr.scale(0.3,0.3,1.89),tr.translate(1,1,0.5)])
    torre66_2.childs += [gpuBox]

    torre66 = sg.SceneGraphNode("torre66")
    torre66.transform = tr.identity()
    torre66.childs += [torre66_1, torre66_2]

    #torre 90
    torre90_1 = sg.SceneGraphNode("torre90_1")
    torre90_1.transform = tr.matmul([tr.scale(0.3,0.3,2.576),tr.translate(0,-1,0.5)])
    torre90_1.childs += [gpuBox]


    torre90_2 = sg.SceneGraphNode("torre90_2")
    torre90_2.transform = tr.matmul([tr.scale(0.3,0.3,2.576),tr.translate(0,1,0.5)])
    torre90_2.childs += [gpuBox]


    torre90_3 = sg.SceneGraphNode("torre90_3")
    torre90_3.transform = tr.matmul([tr.scale(0.3,0.3,2.576),tr.translate(1,0,0.5)])
    torre90_3.childs += [gpuBox]


    torre90 = sg.SceneGraphNode("torre90")
    torre90.transform = tr.identity()
    torre90.childs += [torre90_1, torre90_2, torre90_3]

    #torre 108
    torre108_1 = sg.SceneGraphNode("torre108_1")
    torre108_1.transform = tr.matmul([tr.scale(0.3,0.3,3.094),tr.translate(0,0,0.5)])
    torre108_1.childs += [gpuBox]


    torre108_2 = sg.SceneGraphNode("torre108_2")
    torre108_2.transform = tr.matmul([tr.scale(0.3,0.3,3.094),tr.translate(-1,0,0.5)])
    torre108_2.childs += [gpuBox]

    torre108 = sg.SceneGraphNode("torre108")
    torre108.transform = tr.identity()
    torre108.childs += [torre108_1, torre108_2]

    #willis tower
    willis = sg.SceneGraphNode("willis")
    willis.transform = tr.uniformScale(0.5)
    willis.childs += [torre50, torre66, torre90, torre108]

    return willis

def burj(pipeline):

    #Nota al ayudante: No pude entender curvas antes de la entrega, gg:(

    #edificio
    shapeBox = bs.createTextureNormalsCube("burj.jpg")
    gpuBox = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBox)
    gpuBox.texture = es.textureSimpleSetup(
        getAssetPath("burj.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuBox.fillBuffers(shapeBox.vertices, shapeBox.indices, GL_STATIC_DRAW)

    shapeBox2 = bs.createTextureNormalsCube("pholder_w.jpg")
    gpuBox2 = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBox2)
    gpuBox2.texture = es.textureSimpleSetup(
        getAssetPath("pholder_w.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuBox2.fillBuffers(shapeBox2.vertices, shapeBox2.indices, GL_STATIC_DRAW)

    #ed1
    ed1 = sg.SceneGraphNode("ed1")
    ed1.transform = tr.matmul([tr.rotationZ(0.44),tr.scale(0.25,1.2,3.094),tr.translate(-1.5,0,0.5)])
    ed1.childs += [gpuBox]

    #ed2
    ed2 = sg.SceneGraphNode("ed1")
    ed2.transform = tr.matmul([tr.rotationZ(-0.44),tr.scale(0.25,1.2,3.094),tr.translate(1.5,0,0.5)])
    ed2.childs += [gpuBox]

    #tapa
    tapa = sg.SceneGraphNode("tapa")
    tapa.transform = tr.matmul([tr.scale(0.4,0.01,3.5),tr.translate(0,-75,0.5)])
    tapa.childs += [gpuBox2]

    #burj
    burj = sg.SceneGraphNode("burj")
    burj.transform = tr.uniformScale(0.35)
    burj.childs += [ed1, ed2, tapa]


    return burj

def cachos_burj(pipeline,R0,R1,R2,R3,N=50):
    
    #Puntos Bezier
    R0 = np.array([[0.07008468, -0.25957928,  1.2246171 ]]).T
    R1 = np.array([[0.37271957, 0.40544627, 1.12587733]]).T
    R2 = np.array([[0.21996678, 0.13868585, 1.1708493]]).T
    R3 = np.array([[0.2356832, 0.17104545, -0.08064855]]).T

    shapeCacho = bs.CurvaBezier(R0,R1,R2,R3,N)
    gpuCacho = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCacho)
    gpuCacho.fillBuffers(shapeCacho.vertices, shapeCacho.indices, GL_STATIC_DRAW)
        
    cacho = sg.SceneGraphNode("cacho")
    cacho.transform = tr.identity()
    cacho.childs += [gpuCacho]

    return cacho




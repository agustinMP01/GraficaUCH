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
        skybox.transform = tr.matmul([tr.translate(0, 0, 0.3), tr.uniformScale(2)])
        skybox.childs += [gpuSky]

        self.model = skybox

    def draw(self,pipeline,projection,view):
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    
        sg.drawSceneGraphNode(self.model, pipeline, "model")
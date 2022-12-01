# coding=utf-8
"""Tarea 2"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.easy_shaders as es
import grafica.lighting_shaders as ls
import grafica.performance_monitor as pm
from grafica.assets_path import getAssetPath

__author__ = "Ivan Sipiran"
__license__ = "MIT"

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True
        self.viewPos = np.array([10,10,10])
        self.camUp = np.array([0, 1, 0])
        self.distance = 10


controller = Controller()

def setPlot(pipeline, mvpPipeline):
    projection = tr.perspective(45, float(width)/float(height), 0.1, 100)

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "La"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ls"), 1.0, 1.0, 1.0)

    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "lightPosition"), 5, 5, 5)
    
    glUniform1ui(glGetUniformLocation(pipeline.shaderProgram, "shininess"), 1000)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "constantAttenuation"), 0.001)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "linearAttenuation"), 0.1)
    glUniform1f(glGetUniformLocation(pipeline.shaderProgram, "quadraticAttenuation"), 0.01)

def setView(pipeline, mvpPipeline):
    view = tr.lookAt(
            controller.viewPos,
            np.array([0,0,0]),
            controller.camUp
        )

    glUseProgram(mvpPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    glUniform3f(glGetUniformLocation(pipeline.shaderProgram, "viewPosition"), controller.viewPos[0], controller.viewPos[1], controller.viewPos[2])
    

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_LEFT_CONTROL:
        controller.showAxis = not controller.showAxis

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    
    elif key == glfw.KEY_1:
        controller.viewPos = np.array([controller.distance,controller.distance,controller.distance]) #Vista diagonal 1
        controller.camUp = np.array([0,1,0])
    
    elif key == glfw.KEY_2:
        controller.viewPos = np.array([0,0,controller.distance]) #Vista frontal
        controller.camUp = np.array([0,1,0])

    elif key == glfw.KEY_3:
        controller.viewPos = np.array([controller.distance,0,controller.distance]) #Vista lateral
        controller.camUp = np.array([0,1,0])

    elif key == glfw.KEY_4:
        controller.viewPos = np.array([0,controller.distance,0]) #Vista superior
        controller.camUp = np.array([1,0,0])
    
    elif key == glfw.KEY_5:
        controller.viewPos = np.array([controller.distance,controller.distance,-controller.distance]) #Vista diagonal 2
        controller.camUp = np.array([0,1,0])
    
    elif key == glfw.KEY_6:
        controller.viewPos = np.array([-controller.distance,controller.distance,-controller.distance]) #Vista diagonal 2
        controller.camUp = np.array([0,1,0])
    
    elif key == glfw.KEY_7:
        controller.viewPos = np.array([-controller.distance,controller.distance,controller.distance]) #Vista diagonal 2
        controller.camUp = np.array([0,1,0])
    
    else:
        print('Unknown key')

def createGPUShape(pipeline, shape):
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)

    return gpuShape

#NOTA: Aqui creas tu escena. En escencia, sólo tendrías que modificar esta función.
def createScene(pipeline):
    #primitivas 
    
    sphere = createGPUShape(pipeline, bs.createColorSphereTarea2(0.152, 0.149, 0.149))
    cone = createGPUShape(pipeline, bs.createColorConeTarea2(1.0,0.73,0.03))
    cube = createGPUShape(pipeline, bs.createColorCubeTarea2(0.431, 0.431, 0.431))
    cylinder = createGPUShape(pipeline, bs.createColorCylinderTarea2(0.074, 0.184, 0.705))
    #para los manubrios
    cylinder1 = createGPUShape(pipeline, bs.createColorCylinderTarea2(0.286, 0.094, 0.094))
    #para los pedales
    cube1 = createGPUShape(pipeline, bs.createColorCubeTarea2(0.549, 0.509, 0.509))



    #-------------------------------------------------------------------------------------------------------------
    #cilindros!
    #palo principal 
    cylinderNode = sg.SceneGraphNode('cylinder')
    #eje y de la escala para alargar el cilindro , la rotacion va en el medio, primero esclamaos antes que todo.
    cylinderNode.transform = tr.matmul([tr.translate(0,4,0),tr.rotationX(np.pi/2), tr.scale(0.2, 4, 0.2)])
    cylinderNode.childs += [cylinder]
    #palo que sostiene la rueda delantera y el manubrio
    cylinderNode1 = sg.SceneGraphNode('cylinder')
    cylinderNode1.transform = tr.matmul([tr.translate(0,-0.5,0.8),tr.rotationX(-np.pi/15),tr.translate(0,4.5,4), tr.scale(0.2, 2.35, 0.2)])
    cylinderNode1.childs += [cylinder]
    #manubrio
    cylinderNode2 = sg.SceneGraphNode('cylinder')
    cylinderNode2.transform = tr.matmul([tr.translate(0,7,3.3),tr.rotationZ(np.pi/2), tr.scale(0.2, 1.8, 0.2)])
    cylinderNode2.childs += [cylinder]

    #partes del manubrio. 
    #1
    cylinderNode11 = sg.SceneGraphNode('cylinder')
    cylinderNode11.transform = tr.matmul([tr.translate(1.5,7,3.3),tr.rotationZ(np.pi/2), tr.scale(0.3, 0.5, 0.3)])
    cylinderNode11.childs += [cylinder1]
    #2
    cylinderNode12 = sg.SceneGraphNode('cylinder')
    cylinderNode12.transform = tr.matmul([tr.translate(-1.5,7,3.3),tr.rotationZ(np.pi/2), tr.scale(0.3, 0.5, 0.3)])
    cylinderNode12.childs += [cylinder1]



    #palo que conecta con el motor y el palo que va el manumbrio (donde va la cadena)
    cylinderNode3 = sg.SceneGraphNode('cylinder')
    cylinderNode3.transform = tr.matmul([tr.translate(0,-0.5,0.85),tr.rotationX(-np.pi/10),tr.translate(0,2,0),tr.rotationX(np.pi/2), tr.scale(0.2, 4, 0.2)])
    cylinderNode3.childs += [cylinder]
    #palo que conceta con el principal y el motor, que sirve para poner el asiento 
    cylinderNode4 = sg.SceneGraphNode('cylinder')
    cylinderNode4.transform = tr.matmul([tr.translate(0,2.7,-4),tr.rotationX(-np.pi/17), tr.scale(0.2, 2.75, 0.2)])
    cylinderNode4.childs += [cylinder]
    #palo que une el motor con la rueda trasera
    #parte 1
    cylinderNode5 = sg.SceneGraphNode('cylinder')
    cylinderNode5.transform = tr.matmul([tr.translate(0.4,0,-5),tr.rotationX(np.pi/2), tr.scale(0.2, 1.65, 0.2)])
    cylinderNode5.childs += [cylinder]
    #parte 2 
    cylinderNode13 = sg.SceneGraphNode('cylinder')
    cylinderNode13.transform = tr.matmul([tr.translate(-0.4,0,-5),tr.rotationX(np.pi/2), tr.scale(0.2, 1.65, 0.2)])
    cylinderNode13.childs += [cylinder]


    #palo trasero , conecta rueda trasera con el palo del asiento 
    cylinderNode6 = sg.SceneGraphNode('cylinder')
    cylinderNode6.transform = tr.matmul([tr.translate(0,3.2,1),tr.rotationX(-np.pi/3),tr.translate(0,5,-3),tr.rotationX(np.pi/2), tr.scale(0.2, 1, 0.2)])
    cylinderNode6.childs += [cylinder]


    #haremos los palos necesarios par amontar las ruedas trasera y delantera. 
    #delantera 1 
    cylinderNode7 = sg.SceneGraphNode('cylinder')
    cylinderNode7.transform = tr.matmul([tr.translate(0,-0.5,0.8),tr.rotationX(-np.pi/15),tr.translate(0.4,1.5,4), tr.scale(0.2, 1.85, 0.2)])
    cylinderNode7.childs += [cylinder]
    #delantera 2 
    cylinderNode8 = sg.SceneGraphNode('cylinder')
    cylinderNode8.transform = tr.matmul([tr.translate(0,-2.5,1.3),tr.rotationX(-np.pi/15),tr.translate(-0.4,3.5,4), tr.scale(0.2, 1.85, 0.2)])
    cylinderNode8.childs += [cylinder]

    #trasera 1 
    cylinderNode9 = sg.SceneGraphNode('cylinder')
    cylinderNode9.transform = tr.matmul([tr.translate(0.4,1.2,0),tr.rotationX(-np.pi/3),tr.translate(-0.1,5,-3),tr.rotationX(np.pi/2), tr.scale(0.2, 1.45, 0.2)])
    cylinderNode9.childs += [cylinder]
    #trasera 2 
    cylinderNode10 = sg.SceneGraphNode('cylinder')
    cylinderNode10.transform = tr.matmul([tr.translate(-0.4,1.2,0),tr.rotationX(-np.pi/3),tr.translate(0.1,5,-3),tr.rotationX(np.pi/2), tr.scale(0.2, 1.45, 0.2)])
    cylinderNode10.childs += [cylinder]
    #cosito que va en el motor de la bici 
    cylinderNode14 = sg.SceneGraphNode('cylinder')
    cylinderNode14.transform = tr.matmul([tr.translate(0.2,0,-3.5),tr.rotationZ(np.pi/2), tr.scale(0.4, 1, 0.4)])
    cylinderNode14.childs += [cylinder]
    #cosito que va en la rueda delantera 
    cylinderNode15 = sg.SceneGraphNode('cylinder')
    cylinderNode15.transform = tr.matmul([tr.translate(0,0,4.75),tr.rotationZ(np.pi/2), tr.scale(0.4, 0.6, 0.4)])
    cylinderNode15.childs += [cylinder]
    #pata de cambio
    #parte 1 
    cylinderNode16 = sg.SceneGraphNode('cylinder')
    cylinderNode16.transform = tr.matmul([tr.translate(0.5,0.345,-6.5),tr.rotationZ(np.pi/2), tr.scale(0.5, 0.5, 0.5)])
    cylinderNode16.childs += [cylinder] 
    #parte 2 
    cylinderNode17 = sg.SceneGraphNode('cylinder')
    cylinderNode17.transform = tr.matmul([tr.translate(0.5,-0.45,-6.9),tr.rotationZ(np.pi/2), tr.scale(0.3, 0.5, 0.3)])
    cylinderNode17.childs += [cylinder]  
    #parte que sostienen los pedales  
    #Parte 1 
    cylinderNode18 = sg.SceneGraphNode('cylinder')
    cylinderNode18.transform = tr.matmul([tr.translate(1,0.8,-3.8),tr.rotationX(-np.pi/10), tr.scale(0.15, 1.1, 0.15)])
    cylinderNode18.childs += [cylinder] 
    #parte 2 
    cylinderNode19 = sg.SceneGraphNode('cylinder')
    cylinderNode19.transform = tr.matmul([tr.translate(-0.5,-1,-3.2),tr.rotationX(1.9*np.pi), tr.scale(0.15, 1, 0.15)])
    cylinderNode19.childs += [cylinder] 
#-----------------------------------------------------------------------------------------------------
    #cubos
    #asiento 
    cubeNode = sg.SceneGraphNode('cube')
    cubeNode.transform = tr.matmul([tr.translate(0,5.5,-4.5),tr.scale(0.45, 0.1, 0.8)])
    cubeNode.childs += [cube]
    #pedal 1 
    cubeNode1 = sg.SceneGraphNode('cube')
    cubeNode1.transform = tr.matmul([tr.translate(1.4,1.83,-4),tr.uniformScale(0.6),tr.scale(0.8, 0.1, 0.45)])
    cubeNode1.childs += [cube1]
    #pedal 2 
    cubeNode2 = sg.SceneGraphNode('cube')
    cubeNode2.transform = tr.matmul([tr.translate(-0.8,-1.9,-2.8),tr.uniformScale(0.6),tr.scale(0.8, 0.1, 0.45)])
    cubeNode2.childs += [cube1]
    
#----------------------------------------------------------------------------------------------------------------------------
    #esferas 
    #rueda delantera 
    sphereNode = sg.SceneGraphNode('cube')
    sphereNode.transform = tr.matmul([tr.translate(0,0,4.75),tr.scale(0.2, 2.3, 2.3)])
    sphereNode.childs += [sphere]
    #rueda trasera 
    sphereNode1 = sg.SceneGraphNode('cube')
    sphereNode1.transform = tr.matmul([tr.translate(0,0,-6.5),tr.scale(0.2, 2.3, 2.3)])
    sphereNode1.childs += [sphere]
    #motor de la bici 
    sphereNode2 = sg.SceneGraphNode('cube')
    sphereNode2.transform = tr.matmul([tr.translate(0.8,0,-3.5),tr.scale(0.05, 1,1)])
    sphereNode2.childs += [sphere]
    #----------------------------------------------------------------------------------------------
    #vamos a dejar todo lo que es esqueleto de la bici en un nodo distinto y a las ruedas tambien  que tendran como padre la bicicleta 
    esqueleto= sg.SceneGraphNode("esqueleto")
    esqueleto.childs += [cylinderNode]
    esqueleto.childs += [cylinderNode1]
    esqueleto.childs += [cylinderNode2]
    esqueleto.childs += [cylinderNode3]
    esqueleto.childs += [cylinderNode4]
    esqueleto.childs += [cylinderNode5]
    esqueleto.childs += [cylinderNode6]
    esqueleto.childs += [cylinderNode7]
    esqueleto.childs += [cylinderNode8]
    esqueleto.childs += [cylinderNode9]
    esqueleto.childs += [cylinderNode10]
    esqueleto.childs += [cylinderNode11]
    esqueleto.childs += [cylinderNode12]
    esqueleto.childs += [cylinderNode13]
    esqueleto.childs += [cylinderNode14]
    esqueleto.childs += [cylinderNode15]
    esqueleto.childs += [cylinderNode16]
    esqueleto.childs += [cylinderNode17]
    esqueleto.childs += [cylinderNode18]
    esqueleto.childs += [cylinderNode19]
    #cubos 
    esqueleto.childs += [cubeNode]
    esqueleto.childs += [cubeNode1]
    esqueleto.childs += [cubeNode2]
    #esferas
    esqueleto.childs += [sphereNode2]
#--------------------------------------------------------------------------------------------------------------------------------
    #esferas 
    ruedas= sg.SceneGraphNode("esqueleto")
    ruedas.childs += [sphereNode]
    ruedas.childs += [sphereNode1]

#---------------------------------------------------------------------------------------------------------------------------------
#ensamble de la bici 
    bicicleta= sg.SceneGraphNode("bicicleta")
    bicicleta.childs += [esqueleto]
    bicicleta.childs += [ruedas]

#--------------------------------------------------------------------------------------------------------------------------------
    #"cabeza" del grafo   
    scene = sg.SceneGraphNode('system')
    scene.childs += [bicicleta]

#--------------------------------------------------------------------------------------------------------------------------------
#de esta manera queda nuetro arbol totalmente definido , ya que tenemos en la cúspide la cabeza de la escena y de acá para abajo se va 
#construyendo todo , como primer nodo interno (el mas cercano al nodo escena)tenemos el nodo bicicleta , de aca salen dos internos mas, 
#el nodo esqueleto y el nodo ruedas que a su vez de estos dos nodos salen los nodos que contienen las figuras para finalmente llegar a las 
#hojas.
    return scene
if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 1000
    height = 1000
    title = "Tarea 2"
    window = glfw.create_window(width, height, title, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Assembling the shader program (pipeline) with both shaders
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()
    pipeline = ls.SimpleGouraudShaderProgram()
    
    # Telling OpenGL to use our shader program
    glUseProgram(mvpPipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory
    cpuAxis = bs.createAxis(7)
    gpuAxis = es.GPUShape().initBuffers()
    mvpPipeline.setupVAO(gpuAxis)
    gpuAxis.fillBuffers(cpuAxis.vertices, cpuAxis.indices, GL_STATIC_DRAW)

    #NOTA: Aqui creas un objeto con tu escena
    dibujo = createScene(pipeline)

    setPlot(pipeline, mvpPipeline)

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    while not glfw.window_should_close(window):

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, title + str(perfMonitor))

        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        setView(pipeline, mvpPipeline)

        if controller.showAxis:
            glUseProgram(mvpPipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            mvpPipeline.drawCall(gpuAxis, GL_LINES)

        #NOTA: Aquí dibujas tu objeto de escena
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNode(dibujo, pipeline, "model")
        

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuAxis.clear()
    dibujo.clear()
    

    glfw.terminate()
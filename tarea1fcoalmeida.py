import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy 
import sys
__author__ = "Ivan Sipiran"
__license__ = "MIT"

# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4

def crear_dama(x,y,r,g,b,radius):
    
    circle = []
    for angle in range(0,360,10):
        circle.extend([x, y, 0.0, r, g, b])
        circle.extend([x+numpy.cos(numpy.radians(angle))*radius, 
                       y+numpy.sin(numpy.radians(angle))*radius, 
                       0.0, r, g, b])
        circle.extend([x+numpy.cos(numpy.radians(angle+10))*radius, 
                       y+numpy.sin(numpy.radians(angle+10))*radius, 
                       0.0, r, g, b])
    
    return numpy.array(circle, dtype = numpy.float32)
    #aca hacemos el molde con el que haremos todos los cuadrados necesarios para el tablero. 
    
def cuadradito(x,y,r,g,b,largo):
    cuad = []
    cuad.extend([x+largo,y+largo,0,r,g,b])
    cuad.extend([x-largo,y+largo,0,r,g,b])
    cuad.extend([x+largo,y-largo,0,r,g,b])
    cuad.extend([x-largo,y-largo,0,r,g,b])
    cuad.extend([x-largo,y+largo,0,r,g,b])
    cuad.extend([x+largo,y-largo,0,r,g,b])

    return numpy.array(cuad,dtype=numpy.float32)
if __name__ == "__main__":

    # Initialize glfw
    window = None
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Tarea 1 Francisco Almeida Díaz", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)



    # Defining shaders for our pipeline
    vertex_shader = """
    #version 330
    in vec3 position;
    in vec3 color;

    out vec3 newColor;
    void main()
    {
        gl_Position = vec4(position, 1.0f);
        newColor = color;
    }
    """

    fragment_shader = """
    #version 330
    in vec3 newColor;

    out vec4 outColor;
    void main()
    {
        outColor = vec4(newColor, 1.0f);
    }
    """
    

    # Binding artificial vertex array object for validation
    
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # Assembling the shader program (pipeline) with both shaders
    shaderProgram = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    #definimos los buffers a utilizar

    #necesitamos 32 cuadraditos negros
    vboNegro = glGenBuffers(32)
    #son 24 damas 
    vboDama = glGenBuffers(24)
    #hacemos nuestros cuadraditos negros. 
    #fila    
    m = 0
    #columna 
    n = 0 
    #contador
    j = 0 
    f = numpy.arange(0,8)
    g = numpy.arange(0,4)
    for m in f : 
        for n in g:
            if(m%2==0):
                Negro = cuadradito(-0.875 + (0.5*n),0.875 -(0.25*m) ,0,0,0,0.125)
                glBindBuffer(GL_ARRAY_BUFFER, vboNegro[j])
                glBufferData(GL_ARRAY_BUFFER, len(Negro) * SIZE_IN_BYTES, Negro, GL_STATIC_DRAW)
                j = j + 1
            else: 

                Negro = cuadradito(-0.625 + (0.5*n),0.625 -(0.25*(m-1)) ,0,0,0,0.125)
                glBindBuffer(GL_ARRAY_BUFFER, vboNegro[j])
                glBufferData(GL_ARRAY_BUFFER, len(Negro) * SIZE_IN_BYTES, Negro, GL_STATIC_DRAW)
                j = j + 1 

    #hacemos nuestras damas 
    m1 = 0 
    n1 = 0 
    j1 = 0 

    for m1 in f : 
        for n1 in g:
            if(m1%2==0):
                if (m1 < 3):
                    
                    Dama = crear_dama(-0.875 + (0.5*n1),0.875 -(0.25*m1) ,1,0,0,0.0625)
                    glBindBuffer(GL_ARRAY_BUFFER, vboDama[j1])
                    glBufferData(GL_ARRAY_BUFFER, len(Dama) * SIZE_IN_BYTES, Dama, GL_STATIC_DRAW)


                    j1 = j1 + 1
                if m1 > 4: 
                    Dama = crear_dama(-0.875 + (0.5*n1),0.875 -(0.25*m1) ,0,0,1,0.0625)
                    glBindBuffer(GL_ARRAY_BUFFER, vboDama[j1])
                    glBufferData(GL_ARRAY_BUFFER, len(Dama) * SIZE_IN_BYTES, Dama, GL_STATIC_DRAW)
                    j1 = j1 + 1
            else: 

                if (m1 < 3):
                    Dama = crear_dama(-0.625 + (0.5*n1),0.625 -(0.25*(m1-1)) ,1,0,0,0.0625)
                    glBindBuffer(GL_ARRAY_BUFFER, vboDama[j1])
                    glBufferData(GL_ARRAY_BUFFER, len(Dama) * SIZE_IN_BYTES, Dama, GL_STATIC_DRAW)
                    j1 = j1 + 1
                if m1 > 4: 
                    Dama = crear_dama(-0.625 + (0.5*n1),0.625 -(0.25*(m1-1)) ,0,0,1,0.0625)
                    glBindBuffer(GL_ARRAY_BUFFER, vboDama[j1])
                    glBufferData(GL_ARRAY_BUFFER, len(Dama) * SIZE_IN_BYTES, Dama, GL_STATIC_DRAW)

                    j1 = j1 + 1


    # Telling OpenGL to use our shader program
    glUseProgram(shaderProgram)

    # Setting up the clear screen color

    #cambiamos de color el fondo y lo hacemos blanco.
    #había creado un cuadrado de 1x1 blanco para usarlo 
    #pero luego pensé en usar esta funcion , que cambia el color del fondo
    #asi en vez de hacer ese cuadrado lo hice con el fondo blanco, 
    # no se si será peor o mejor pero me imagino que entre menos lineas de codigo mejor 
    #o no ? 

    glClearColor(1,1,1,1.0)

    glClear(GL_COLOR_BUFFER_BIT)

    #indicamos como tiene que ir a sacar la data de los buffers para el caso del cualdrado y 
    #de la dama. 

    i = 0
    while i < 32: 


        glBindBuffer(GL_ARRAY_BUFFER, vboNegro[i])  
        position = glGetAttribLocation(shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)

        color = glGetAttribLocation(shaderProgram, "color")
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)
        glDrawArrays(GL_TRIANGLES,0,6)
        i = i + 1 

    k = 0 
    while k < 24: 


        glBindBuffer(GL_ARRAY_BUFFER, vboDama[k])  
        position = glGetAttribLocation(shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)

        color = glGetAttribLocation(shaderProgram, "color")
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)
        glDrawArrays(GL_TRIANGLES,0,108)
        k = k + 1 

    # Moving our draw to the active color buffer
    glfw.swap_buffers(window)

    # Waiting to close the window
    while not glfw.window_should_close(window):

        # Getting events from GLFW
        glfw.poll_events()
        
    glfw.terminate()

  

            


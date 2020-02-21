from OpenGL.GL import *
import math
import numpy

class ObjLoader(object):
    def __init__(self, fileName):
        self.vertices = list()
        self.faces = list()
        try:
            file = open(fileName)
            for line in file:
                if line.startswith('v '):
                    line = line.strip().split()
                    vertex = (float(line[1]), float(line[2]), float(line[3]) )
                    vertex = (round(vertex[0], 2), round(vertex[1], 2), round(vertex[2], 2))
                    self.vertices.append(vertex)

                elif line.startswith('f'):
                    line = line.strip().split()
                    line[1].split('/')[0]
                    if '/' in line[1]:
                        line[1] = line[1].split('/')[0]
                    if '/' in line[2]:
                        line[2] = line[2].split('/')[0]
                    if '/' in line[3]:
                        line[3] = line[3].split('/')[0]
                    face = (int(line[1]), int(line[2]), int(line[3]) )
                    self.faces.append(face)
            file.close()
        except IOError:
            print(".obj file not found.")

    def render_scene(self):
        if len(self.faces) > 0:
            glRotatef(15.0, 0.0, 0.0, 1.0)
            glBegin(GL_TRIANGLES)
            #glBegin(GL_TRIANGLE_FAN)
            for face in self.faces:
                i = 0
                vertex1 = 0
                vertex2 = 0
                vertex3 = 0
                for f in face:  
                    vertexDraw = self.vertices[int(f) - 1]
                    #make vertex set in face
                    if(i == 0):
                        vertex1 = vertexDraw
                        i += 1
                    elif(i == 1):
                        vertex2 = vertexDraw
                        i += 1
                    elif(i == 2):
                        vertex3 = vertexDraw
                        i = 0
                #make vectors
                vector1 = numpy.subtract(vertex2, vertex1)
                vector2 = numpy.subtract(vertex3, vertex1)
                #Compute normal
                normal = numpy.cross(vector1, vector2)
                #Compute normalized sum
                divider = math.sqrt(normal[0] * normal[0] + normal[1]*normal[1] + normal[2]*normal[2])

                glColor4f(math.fabs(normal[0]/divider), math.fabs(normal[1]/divider), math.fabs(normal[2]/divider), 1.0)

                glVertex3fv(vertex1)
                glVertex3fv(vertex2)
                glVertex3fv(vertex3)
            glEnd()
            ##

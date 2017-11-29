import pygame, pygame.gfxdraw
import sys, math
from camera import Cam

cam = Cam()

class Axis(object):
    def __init__(self, color):
        self.vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
        self.edges = [(0, 1), (0, 2), (0, 3)]
        self.color = color
    def display(self, surface):
        for edge in self.edges:
            points = []
            for x, y, z in [self.vertices[edge[0]], self.vertices[edge[1]]]:
                x, y = x * math.cos(cam.rotation[0]) - y * math.sin(cam.rotation[0]), y * math.cos(cam.rotation[0]) + x * math.sin(cam.rotation[0])
                x, z = x * math.cos(cam.rotation[1]) - z * math.sin(cam.rotation[1]), z * math.cos(cam.rotation[1]) + x * math.sin(cam.rotation[1])
                amp = pygame.Surface.get_width(surface) // 30
                px, py = y * amp, - z * amp
                points += [((pygame.Surface.get_width(surface) - 60) + int(px), 60 + int(py))]
            pygame.gfxdraw.line(surface, points[0][0], points[0][1], points[1][0], points[1][1], self.color)

class Solid(object):
    def __init__(self, color, center):
        # the brightest color on the object
        self.color0 = color
        # center
        self.cx, self.cy, self.cz = center
    def wireFrame(self, surface):
        for edge in self.edges:
            points = []
            isOnScreen = False
            for x, y, z in [self.vertices[edge[0]], self.vertices[edge[1]]]:

                x, y = x * math.cos(cam.rotation[0]) - y * math.sin(cam.rotation[0]), y * math.cos(cam.rotation[0]) + x * math.sin(cam.rotation[0])
                x, z = x * math.cos(cam.rotation[1]) - z * math.sin(cam.rotation[1]), z * math.cos(cam.rotation[1]) + x * math.sin(cam.rotation[1])

                x -= cam.position[0]
                y -= cam.position[1]
                z -= cam.position[2]
                
                if x < 0:
                    isOnScreen = True
                
                depth = -1 / x if x != 0 else -2 ** 5
                amp = pygame.Surface.get_width(surface) * 2 // 3
                px, py = y * depth * amp, - z * depth * amp
                points += [(int(pygame.Surface.get_width(surface) * 0.7 + px), int(pygame.Surface.get_height(surface) / 3 + py))]
            
            if isOnScreen:
                pygame.gfxdraw.line(surface, points[0][0], points[0][1], points[1][0], points[1][1], self.color0)
    # rotation: tuple of angle of rotation on XY plane and XZ plane
    def rotate(self, rotation = (0,0)):
        self.rotateXY(rotation)
        self.rotateXZ(rotation)
    def rotateXY(self, rotation):
        for i in range(len(self.vertices)):
            x, y, z = self.vertices[i]
            x, y = x * math.cos(rotation[0]) - y * math.sin(rotation[0]), y * math.cos(rotation[0]) + x * math.sin(rotation[0])
            self.vertices[i] = x, y, z
    def rotateXZ(self, rotation):
        for i in range(len(self.vertices)):
            x, y, z = self.vertices[i]
            x, z = x * math.cos(rotation[1]) - z * math.sin(rotation[1]), z * math.cos(rotation[1]) + x * math.sin(rotation[1])
            self.vertices[i] = x, y, z
    # scaling: tuple of scale factor for x, y, z dimension
    def scale(self, scaling = (1,1,1)):
        self.scaleX(scaling)
        self.scaleY(scaling)
        self.scaleZ(scaling)
    def scaleX(self, scaling):
        for i in range(len(self.vertices)):
            x, y, z = self.vertices[i]
            x = self.cx + (x - self.cx) * scaling[0]
            self.vertices[i] = x, y, z
    def scaleY(self, scaling):
        for i in range(len(self.vertices)):
            x, y, z = self.vertices[i]
            y = self.cy + (y - self.cy) * scaling[1]
            self.vertices[i] = x, y, z
    def scaleZ(self, scaling):
        for i in range(len(self.vertices)):
            x, y, z = self.vertices[i]
            z = self.cz + (z - self.cz) * scaling[2]
            self.vertices[i] = x, y, z

class Prism(Solid):
    # numSides: the number of sides the base of the solid has
    # sideLen: the length of each side of the base
    # height: the height of the prism
    def __init__(self, color, center, numSides, sideLen, height):
        # get color and center
        super().__init__(color, center)
        
        # side length of the base, height
        self.sideLen = sideLen
        self.height = height
        
        self.numSides = numSides
        
        # calculate a list of the coordinates of vertices
        # calculate a list of connecting vertices that form an edge
        self.vertices = []
        self.edges = []

        z0, z1 = self.cz - self.height / 2, self.cz + self.height / 2
        angle = 2 * math.pi / self.numSides
        radius = self.sideLen / 2 / math.sin(angle / 2)

        for i in range(self.numSides):
            x, y = self.cx + radius * math.cos(angle * i), self.cy + radius * math.sin(angle * i)
            vert = [(x, y, z0), (x, y, z1)]
            self.vertices.extend(vert)
            conn = [(2 * i, 2 * i + 1), (2 * i, (2 * i + 2) % (self.numSides * 2)), (2 * i + 1, (2 * i + 3) % (self.numSides * 2))]
            self.edges.extend(conn)

class Pyramid(Solid):
    # numSides: the number of sides the base of the solid has
    # sideLen: the length of each side of the base
    # height: the height of the pyramid
    def __init__(self, color, center, numSides, sideLen, height):
        # get color and center
        super().__init__(color, center)
        
        # side length of the base, height
        self.sideLen = sideLen
        self.height = height
        
        self.numSides = numSides

        # calculate a list of the coordinates of vertices
        # calculate a list of connecting vertices that form an edge
        self.vertices = []
        self.edges = []

        z0, z1 = self.cz - self.height / 2, self.cz + self.height / 2
        angle = 2 * math.pi / self.numSides
        radius = self.sideLen / 2 / math.sin(angle / 2)

        for i in range(self.numSides):
            x, y = self.cx + radius * math.cos(angle * i), self.cy + radius * math.sin(angle * i)
            vert = [(x, y, z0)]
            self.vertices.extend(vert)
            conn = [(i, self.numSides), (i, (i + 1) % (self.numSides))]
            self.edges.extend(conn)
        self.vertices.append((self.cx, self.cy, z1))

class Polyhedron(Solid):
    # only takes in right polyhedrons: Tetrahedron, Cube, Octahedron, Dodecahedron, Icosahedron
    # numSides: the number of sides the base of the solid has
    # sideLen: the length of each side of the base
    def __init__(self, color, center, numFaces, sideLen):
        # get color and center
        super().__init__(color, center)
        
        # side length of a surface
        self.sideLen = sideLen
        
        # number of sides per surface
        self.numFaces = numFaces
        if self.numFaces not in [4, 6, 8, 12, 20]:
            raise Exception("not a regular polyhedron")
        
        # calculate a list of the coordinates of vertices
        # calculate a list of connecting vertices that form an edge
        shapes = {4: "Tetrahedron", 6: "Cube", 8: "Octahedron", 12: "Dodecahedron", 20: "Icosahedron"}

        self.vertices, self.edges = eval("self." + shapes[numFaces] + "()")

    def Tetrahedron(self):
        self.vertices = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
        self.edges = [(0, 1), (0, 2), (0, 3), (1, 2), (2, 3), (3, 1)]
        for i in range(len(self.vertices)):
            x, y, z = self.vertices[i]
            x = self.cx + x * self.sideLen / math.sqrt(2) / 2
            y = self.cy + y * self.sideLen / math.sqrt(2) / 2
            z = self.cz + z * self.sideLen / math.sqrt(2) / 2
            self.vertices[i] = x, y, z
        return self.vertices, self.edges
    
    def Cube(self):
        self.vertices = [(1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, 1, 1), (1, 1, -1), (1, -1, -1), (-1, -1, -1), (-1, 1, -1)]
        self.edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
        for i in range(len(self.vertices)):
            x, y, z = self.vertices[i]
            x = self.cx + x * self.sideLen / 2
            y = self.cy + y * self.sideLen / 2
            z = self.cz + z * self.sideLen / 2
            self.vertices[i] = x, y, z
        return self.vertices, self.edges
    def Octahedron(self):
        self.vertices = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (0, -1, 0), (0, 0, -1), (-1, 0, 0)]
        self.edges = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (2, 3), (3, 4), (4, 1), (1, 5), (2, 5), (3, 5), (4, 5)]
        for i in range(len(self.vertices)):
            x, y, z = self.vertices[i]
            x = self.cx + x * self.sideLen / math.sqrt(2)
            y = self.cy + y * self.sideLen / math.sqrt(2)
            z = self.cz + z * self.sideLen / math.sqrt(2)
            self.vertices[i] = x, y, z
        return self.vertices, self.edges
    def Dodecahedron(self):
        # golden ratio and its inverse
        phi = (1 + 5 ** 0.5) / 2
        phiI = (5 ** 0.5 - 1) / 2

        self.vertices = [(1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1), 
                         (-1, 1, 1), (-1, 1, -1), (-1, -1, 1), (-1, -1, -1),
                         (phi, 0, phiI), (phi, 0, -phiI), (-phi, 0, phiI), (-phi, 0, -phiI), 
                         (phiI, phi, 0), (-phiI, phi, 0), (phiI, -phi, 0), (-phiI, -phi, 0),
                         (0, phiI, phi), (0, -phiI, phi), (0, phiI, -phi), (0, -phiI, -phi), 
                         ]
        self.edges = [(0, 8), (1, 9), (2, 8), (3, 9), 
                      (4, 10), (5, 11), (6, 10), (7, 11), 
                      (0, 12), (4, 13), (1, 12), (5, 13), 
                      (2, 14), (6, 15), (3, 14), (7, 15),
                      (0, 16), (2, 17), (4, 16), (6, 17), 
                      (1, 18), (3, 19), (5, 18), (7, 19),
                      (8, 9), (10, 11), (12, 13), 
                      (14, 15), (16, 17), (18, 19)]
        for i in range(len(self.vertices)):
            x, y, z = self.vertices[i]
            x = self.cx + x * self.sideLen / math.sqrt(2)
            y = self.cy + y * self.sideLen / math.sqrt(2)
            z = self.cz + z * self.sideLen / math.sqrt(2)
            self.vertices[i] = x, y, z
        return self.vertices, self.edges
    def Icosahedron(self):
        # golden ratio
        phi = (1 + 5 ** 0.5) / 2
        self.vertices = [(0, 1, phi), (0, -1, phi), (0, 1, -phi), (0, -1, -phi), 
                         (1, phi, 0), (-1, phi, 0), (1, -phi, 0), (-1, -phi, 0),
                         (phi, 0, 1), (phi, 0, -1), (-phi, 0, 1), (-phi, 0, -1)]
        self.edges = [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11),
                      (0, 4), (0, 8), (0, 5), (0, 10), 
                      (2, 4), (2, 9), (2, 5), (2, 11),
                      (1, 6), (1, 8), (1, 7), (1, 10), 
                      (3, 6), (3, 9), (3, 7), (3, 11),
                      (4, 8), (4, 9), (5, 10), (5, 11), 
                      (6, 8), (6, 9), (7, 10), (7, 11)]
        for i in range(len(self.vertices)):
            x, y, z = self.vertices[i]
            x = self.cx + x * self.sideLen / math.sqrt(2)
            y = self.cy + y * self.sideLen / math.sqrt(2)
            z = self.cz + z * self.sideLen / math.sqrt(2)
            self.vertices[i] = x, y, z
        return self.vertices, self.edges

class Sphere(Solid):
    # takes in right polyhedrons: Tetrahedron, Cube, Octahedron, Dodecahedron, Icosahedron
    # numLatitude: number of latitude lines the sphere has from +z to -z, exclude two poles
    # numLongitude: number of longitude lines the sphere has
    def __init__(self, color, center, r, numLatitude, numLongitude):
        # get color and center
        super().__init__(color, center)
        
        # the radius of the sphere
        self.r = r
        
        # side length of a surface
        self.numLatitude = numLatitude
        self.numLongitude = numLongitude

        # calculate a list of the coordinates of vertices
        # calculate a list of connecting vertices that form an edge
        self.vertices = []
        self.edges = []

        northPole = (self.cx, self.cy, self.cz + self.r)
        southPole = (self.cx, self.cy, self.cz - self.r)
        self.vertices.append(northPole)
        self.edges.extend([(0, k + 1) for k in range(self.numLongitude)])
        
        # the angle to +z axis (spherical coordinate)
        phi = math.pi / self.numLatitude
        # when projected on x, y plane, the angle to +x axis (spherical coordinate)
        theta = math.pi * 2 / self.numLongitude

        for i in range(self.numLatitude):
            z = self.cz + self.r * math.cos(phi * i)
            for j in range(self.numLongitude):
                x, y = self.cx + self.r * math.sin(phi * i) * math.cos(theta * j), self.cy - self.r * math.sin(phi * i) * math.sin(theta * j)
                self.vertices.append((x, y, z))
                self.edges.append((i * self.numLongitude + j + 1, i * self.numLongitude + 1 + (j + 1) % self.numLongitude))
                self.edges.append((i * self.numLongitude + j + 1, min(self.numLongitude * self.numLatitude + 1, (i + 1) * self.numLongitude + j + 1)))
        self.vertices.append(southPole)

class Custom(Solid):
    def __init__(self, color, center, numFaces, sideLen):
        # get color and center
        super().__init__(color, center)

        # get a list of the coordinates of vertices from user input
        # get a list of connecting vertices that form an edge from user input
        self.vertices = []
        self.edges = []

class Grid(Solid):
    # unit: unit length of one grid
    # spread: total length of the whole grid
    def __init__(self, color, center, unit, spread):
        # get color and center
        super().__init__(color, center)
        # side length of the base, height
        self.unit = unit
        self.spread = spread
        
        self.numCell = self.spread // self.unit
        r = self.numCell * self.unit
        
        # calculate a list of the coordinates of vertices
        # calculate a list of connecting vertices that form an edge
        self.vertices = []
        self.edges = []
        for i in range(0, self.numCell * 2 + 1):
            v = [(r - i * self.unit, r, 0), (r - i * self.unit, -r, 0), (r, r - i * self.unit, 0), (-r, r - i * self.unit, 0)]
            self.vertices.extend(v)
            self.edges.extend([(4 * i, 4 * i + 1), (4 * i + 2, 4 * i + 3)])
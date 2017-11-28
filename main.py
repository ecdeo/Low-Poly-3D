import pygame, sys, math

class Cam(object):
    # position: tuple of camera position (x, y, z)
    # rotation: angle of rotation on XY plane and XZ plane
    def __init__(self, position = (0, 0, 0), rotation = (0,0)):
        self.position = list(position)
        self.rotation = list(rotation)
    def zoom(self, keys, displacement):
        if keys[pygame.K_q]:
            self.position[0] -= displacement
        if keys[pygame.K_e]:
            self.position[0] += displacement

    def leftRight(self, keys, displacement):
        if keys[pygame.K_d]:
            self.position[1] += displacement
        if keys[pygame.K_a]:
            self.position[1] -= displacement

    def upDown(self, keys, displacement):
        if keys[pygame.K_w]:
            self.position[2] += displacement
        if keys[pygame.K_s]:
            self.position[2] -= displacement

    def rotateXY(self, mouse, angleXY):
        if mouse[0]:
            self.rotation[0] += angleXY
    def rotateXZ(self, mouse, angleXZ):
        if mouse[0]:
            self.rotation[1] -= angleXZ
    
    def update(self, fps, keys, mouse, rel):
        displacement = fps / 50
        angleXY, angleXZ = rel[0] / 200, rel[1] / 200

        cam.zoom(keys, displacement)
        cam.leftRight(keys, displacement)
        cam.upDown(keys, displacement)
        cam.rotateXY(mouse, angleXY)
        cam.rotateXZ(mouse, angleXZ)

class Solid(object):
    def __init__(self, color, center):
        # the brightest color on the object
        self.color0 = color
        # center
        self.cx, self.cy, self.cz = center
    def render(self, surface):
        for edge in self.edges:
            points = []
            for x, y, z in [self.vertices[edge[0]], self.vertices[edge[1]]]:
                x, y = x * math.cos(cam.rotation[0]) - y * math.sin(cam.rotation[0]), y * math.cos(cam.rotation[0]) + x * math.sin(cam.rotation[0])
                x, z = x * math.cos(cam.rotation[1]) - z * math.sin(cam.rotation[1]), z * math.cos(cam.rotation[1]) + x * math.sin(cam.rotation[1])
                x -= cam.position[0]
                y -= cam.position[1]
                z -= cam.position[2]
                
                depth = -1 / x if x != 0 else -1
                amp = 600
                px, py = y * depth * amp, - z * depth * amp
                points += [(360 + int(px), 240 + int(py))]
            pygame.draw.line(surface, (0, 0, 0), points[0], points[1], 1)
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
        super(Prism, self).__init__(color, center)
        
        # side length of the base, height
        self.sideLen = sideLen
        self.height = height
        
        self.numSides = numSides
        
        # get a list of the coordinates of vertices
        # get a list of connecting vertices that form an edge
        # major of calculation happens here
        z0, z1 = self.cz - self.height / 2, self.cz + self.height / 2
        angle = 2 * math.pi / self.numSides
        radius = self.sideLen / 2 / math.sin(angle / 2)
        self.vertices = []
        self.edges = []
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
        
        # get a list of the coordinates of vertices
        # get a list of connecting vertices that form an edge
        # major of calculation happens here
        
        self.vertices = []
        self.edges = []
        # get a list of the coordinates of vertices
        # get a list of connecting vertices that form an edge
        # major of calculation happens here
        z0, z1 = self.cz - self.height / 2, self.cz + self.height / 2
        angle = 2 * math.pi / self.numSides
        radius = self.sideLen / 2 / math.sin(angle / 2)
        self.vertices = []
        self.edges = []
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
        # get a list of the coordinates of vertices
        # get a list of connecting vertices that form an edge
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

black = (0,0,0)
center = (0,0,0)
prism = Prism(black, (0,3,0), 9, 1, 2)
pyramid = Pyramid(black, (0, -3, 0), 5, 2, 2)
tetrahedron = Polyhedron(black, (0,0,0), 12, 1)
cam = Cam(position = (10,0,0), rotation = (0, 0))



# https://qwewy.gitbooks.io/pygame-module-manual/content/chapter1/the-mainloop.html
class Main(object):
    def __init__(self, width = 720, height = 480, fps=10):
        self.width = width
        self.height = height
        self.fps = fps
        self.bgColor = (255, 255, 255)
        self.cam = Cam((5,5,5))
        pygame.init()
    def eventsUpdate(self):
        pass
    
    def graphicsUpdate(self, screen):
        prism.render(screen)
        pyramid.render(screen)
        tetrahedron.render(screen)

    
    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        while True:
            time = clock.tick(self.fps)
            screen.fill(self.bgColor)
            self.graphicsUpdate(screen)
            
            pygame.display.flip()

            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()
            rel = pygame.mouse.get_rel()

            self.cam.update(self.fps, keys, mouse, rel)

            for event in pygame.event.get():
                #  quitting
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
            

def main():
    game = Main()
    game.run()

if __name__ == '__main__':
    main()


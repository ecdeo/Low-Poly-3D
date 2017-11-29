import pygame, pygame.gfxdraw
import sys, math
from gui import *
from display import *


"""
move back and forth: q, e
move up and down: w, s
move left and right: a, d
zoom: mouse scroll
rotate: mouse drag

"""

BLACK = (0, 0, 0)
LIGHTGRAY = (200, 200, 200)
YELLOW = (251, 221, 51)
BLUE = (100, 217, 239)
ORANGE = (255, 220, 150)

solids = [
        Prism(BLACK, (0,3,0), 9, 0.5, 2),
        Pyramid(BLACK, (0, -3, 0), 5, 2, 2),
        Polyhedron(BLACK, (3,0,0), 8, math.sqrt(2)),
        Sphere(BLACK, (0,0,0), 1, 10, 10),
        ]



# https://qwewy.gitbooks.io/pygame-module-manual/content/chapter1/the-mainloop.html
class Main(object):
    def initGui(self):
        # panel
        self.panelWidth = self.width / 5
        self.panel = Panel(self.panelWidth, self.height, ORANGE)
        # button
        iconA = pygame.image.load('iconA.png')
        iconD = pygame.image.load('iconD.png')
        iconA1 = pygame.image.load('iconA1.png')
        iconD1 = pygame.image.load('iconD1.png')
        w, h = iconA.get_size()
        h -= 3
        icon_tutorialA = iconA1.subsurface((0 * h, 0, h, h))
        icon_tutorialD = iconD1.subsurface((0 * h, 0, h, h))
        icon_plusA =     iconA1.subsurface((1 * h, 0, h, h))
        icon_plusD =     iconD1.subsurface((1 * h, 0, h, h))
        icon_homeA =     iconA.subsurface((2 * h, 0, h, h))
        icon_homeD =     iconD.subsurface((2 * h, 0, h, h))
        icon_rotateA =   iconA.subsurface((3 * h, 0, h, h))
        icon_rotateD =   iconD.subsurface((3 * h, 0, h, h))    
        icon_fillA =     iconA.subsurface((4 * h, 0, h, h))
        icon_fillD =     iconD.subsurface((4 * h, 0, h, h))
        icon_wireA =     iconA.subsurface((5 * h, 0, h, h))
        icon_wireD =     iconD.subsurface((5 * h, 0, h, h))
        icon_screenA =   iconA.subsurface((6 * h, 0, h, h))
        icon_screenD =   iconD.subsurface((6 * h, 0, h, h))
        icon_exportA =   iconA.subsurface((7 * h - 2, 0, h, h))
        icon_exportD =   iconD.subsurface((7 * h - 2, 0, h, h))
        self.buttonWidthP = self.width / 30
        self.button_tutorial = Button(10, 10, self.buttonWidthP, self.buttonWidthP, icon_tutorialD, icon_tutorialA)
        self.button_adding =   Button(self.panelWidth - self.buttonWidthP - 10, 10, self.buttonWidthP, self.buttonWidthP, icon_plusD, icon_plusA)
        self.buttonWidthW = self.width / 20
        c, d = self.width * 0.6, self.buttonWidthW * 1.2
        self.button_home =     Button(c - 3 * d, self.height - d, self.buttonWidthW, self.buttonWidthW, icon_homeD, icon_homeA)
        self.button_rotate =   Button(c - 2 * d, self.height - d, self.buttonWidthW, self.buttonWidthW, icon_rotateD, icon_rotateA)    
        self.button_fill =     Button(c - 1 * d, self.height - d, self.buttonWidthW, self.buttonWidthW, icon_fillD, icon_fillA)
        self.button_wire =     Button(c + 0 * d, self.height - d, self.buttonWidthW, self.buttonWidthW, icon_wireD, icon_wireA)
        self.button_screen =   Button(c + 1 * d, self.height - d, self.buttonWidthW, self.buttonWidthW, icon_screenD, icon_screenA)    
        self.button_export =   Button(c + 2 * d, self.height - d, self.buttonWidthW, self.buttonWidthW, icon_exportD, icon_exportA)

        self.buttonList = [
                            self.button_tutorial,
                            self.button_tutorial,
                            self.button_home,
                            self.button_rotate,
                            self.button_fill,
                            self.button_wire,
                            self.button_screen, 
                            self.button_export
                            ]

    def __init__(self, width = 1440, height = 840, fps=10):
        self.width = width
        self.height = height
        self.fps = fps
        self.bgColor = (225, 225, 225)
        self.title = "LowPoly 3D"

        self.grid = Grid(LIGHTGRAY, (0,0,0), unit = 1, spread = 5)
        self.axis = Axis(BLUE)
        self.initGui()
        pygame.init()

    def mousePressed(self, x, y):
        pass

    def mouseMotion(self, x, y, surface):
        for b in self.buttonList:
            if b.isInBound(x, y):
                b.drawA(surface)
    
    def mouseScroll(self, x, y, button):
        if x > self.panelWidth:
            if button == 4:
                cam.zoom(self.displacement)
            if button == 5:
                cam.zoom(-self.displacement)
    
    def mouseDrag(self, x, y):
        if x > self.panelWidth:
            angleXY, angleXZ = self.rel[0] / 200, self.rel[1] / 200
            cam.rotateXY(angleXY)
            cam.rotateXZ(angleXZ)

    def keyPressed(self):
        self.displacement = self.fps / 50
        # cam zoom
        if self.keys[pygame.K_q]:
            cam.forthBack(-self.displacement)
        if self.keys[pygame.K_e]:
            cam.forthBack(self.displacement)
        # cam move left/right
        if self.keys[pygame.K_d]:
            cam.leftRight(self.displacement)
        if self.keys[pygame.K_a]:
            cam.leftRight(-self.displacement)
        # cam move up/down
        if self.keys[pygame.K_s]:
            cam.upDown(self.displacement)
        if self.keys[pygame.K_w]:
            cam.upDown(-self.displacement)

    def timerFired(self, dt):
        pass

    def eventsUpdate(self, surface, clock):
        time = clock.tick(self.fps)
        self.timerFired(time)
        self.rel = pygame.mouse.get_rel()
        self.keys = pygame.key.get_pressed()
        self.keyPressed()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mousePressed(*(event.pos))

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button in [4, 5]:
                self.mouseScroll(*(event.pos), event.button)
            
            elif event.type == pygame.MOUSEMOTION and event.buttons == (0, 0, 0):
                self.mouseMotion(*(event.pos), surface)
            
            elif event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
                self.mouseDrag(*(event.pos))
            
            #  quitting
            elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
    
    def graphicsUpdate(self, screen):
        self.grid.wireFrame(screen)
        
        for s in solids:
            s.wireFrame(screen)
        
        self.axis.display(screen)
        self.panel.draw(screen)
        self.button_tutorial.drawD(screen)
        self.button_adding.drawD(screen)
        self.button_home.drawD(screen)
        self.button_rotate.drawD(screen)
        self.button_fill.drawD(screen)
        self.button_wire.drawD(screen)
        self.button_screen.drawD(screen)
        self.button_export.drawD(screen)
    
    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        

        while True:
            screen.fill(self.bgColor)

            self.graphicsUpdate(screen)
            self.eventsUpdate(screen, clock)
            
            pygame.display.flip()

def main():
    game = Main()
    game.run()

if __name__ == '__main__':
    main()


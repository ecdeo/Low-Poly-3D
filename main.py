import pygame, pygame.gfxdraw
import sys, math, datetime, json
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
        
        # tutorial
        self.screen_tutorial = pygame.image.load('images/tutorial.png').convert_alpha()
        pygame.transform.scale(self.screen_tutorial, (self.width, self.height))
        
        # button
        iconA = pygame.image.load('images/iconA.png').convert_alpha()
        iconD = pygame.image.load('images/iconD.png').convert_alpha()
        iconA1 = pygame.image.load('images/iconA1.png').convert_alpha()
        iconD1 = pygame.image.load('images/iconD1.png').convert_alpha()
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
        
        # top pf the panel
        self.buttonWidthP = self.width / 30
        self.button_tutorial = Button(10, 10, self.buttonWidthP, self.buttonWidthP, icon_tutorialD, icon_tutorialA)
        self.button_adding =   Button(self.panelWidth - self.buttonWidthP - 10, 10, self.buttonWidthP, self.buttonWidthP, icon_plusD, icon_plusA)
        self.buttonWidthW = self.width / 20
        
        # bottom of screen
        c, d = self.width * 0.6, self.buttonWidthW * 1.2
        self.button_home =     Button(c - 3 * d, self.height - d, self.buttonWidthW, self.buttonWidthW, icon_homeD, icon_homeA)
        self.button_rotate =   Button(c - 2 * d, self.height - d, self.buttonWidthW, self.buttonWidthW, icon_rotateD, icon_rotateA)    
        self.button_fill =     Button(c - 1 * d, self.height - d, self.buttonWidthW, self.buttonWidthW, icon_fillD, icon_fillA)
        self.button_wire =     Button(c - 1 * d, self.height - d, self.buttonWidthW, self.buttonWidthW, icon_wireD, icon_wireA)
        self.button_camera =   Button(c + 0 * d, self.height - d, self.buttonWidthW, self.buttonWidthW, icon_screenD, icon_screenA)    
        self.button_export =   Button(c + 1 * d, self.height - d, self.buttonWidthW, self.buttonWidthW, icon_exportD, icon_exportA)

        # button: isDisplaying, isInMode
        self.buttonList = {
                            self.button_tutorial: [True, False],
                            self.button_adding: [True, False],
                            self.button_home: [True, False],
                            self.button_rotate: [True, 0],
                            self.button_fill: [True, False],
                            self.button_wire: [False, True],
                            self.button_camera: [True, False], 
                            self.button_export: [True, False]
                            }

    def __init__(self, width = 1440, height = 840, fps=10):
        self.width = width
        self.height = height
        self.fps = fps
        self.bgColor = (225, 225, 225)
        self.title = "LowPoly 3D"

        self.grid = Grid(LIGHTGRAY, (0,0,0), unit = 1, spread = 5)
        self.axis = Axis(BLUE)

        pygame.init()

    def mousePressed(self, x, y, surface):
        if self.buttonList[self.button_tutorial][1]:
            self.buttonList[self.button_tutorial][1] = False

        if self.button_tutorial.isInBound(x, y):
            self.buttonList[self.button_tutorial][1] = True

        elif self.button_home.isInBound(x, y):
            cam.home()
            self.buttonList[self.button_rotate][1] == 0

        elif self.button_rotate.isInBound(x, y):
            self.buttonList[self.button_rotate][1] = (self.buttonList[self.button_rotate][1] + 1) % 4

        elif self.button_fill.isInBound(x, y):
            self.buttonList[self.button_fill][0] = not self.buttonList[self.button_fill][0]
            self.buttonList[self.button_fill][1] = not self.buttonList[self.button_fill][1]
            self.buttonList[self.button_wire][0] = not self.buttonList[self.button_wire][0]
            self.buttonList[self.button_wire][1] = not self.buttonList[self.button_wire][1]

        elif self.button_camera.isInBound(x, y):
            pygame.image.save(surface, "screenshot " + str(datetime.datetime.now()) + ".jpeg")

        elif self.button_export.isInBound(x,y):
            with open('data ' + str(datetime.datetime.now()) + '.txt', 'w') as outfile:  
                for o in solids:
                    json.dump(o.__dict__, outfile)

    def mouseMotion(self, surface):
        x, y = self.pos
        for b in self.buttonList:
            if self.buttonList[b][0]: 
                if b.isInBound(x, y):
                    b.drawA(surface)
                else: b.drawD(surface)
    
    def mouseScroll(self, x, y, button):
        # not on the panel, zoom
        if x > self.panelWidth:
            if button == 4:
                cam.zoom(self.displacement)
            if button == 5:
                cam.zoom(-self.displacement)

        # in the scroll zone
    
    def mouseDrag(self, x, y):
        if x > self.panelWidth:
            angleXY, angleXZ = self.rel[0] / 200, self.rel[1] / 200
            cam.rotateXY(angleXY)
            cam.rotateXZ(angleXZ)

    def keyPressed(self):
        # when not entering text

        # cam move back/forth
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

        # whe entering text

    def timerFired(self, dt):
        angle = self.displacement / 2
        if self.buttonList[self.button_rotate][1] == 1:
            cam.rotateXY(angle)
        elif self.buttonList[self.button_rotate][1] == 2:
            cam.rotateXZ(angle)
        if self.buttonList[self.button_rotate][1] == 3:
            cam.rotate(angle)

    def eventsUpdate(self, surface, clock):
        time = clock.tick(self.fps)
        self.displacement = self.fps / 50
        self.rel = pygame.mouse.get_rel()
        self.pos = pygame.mouse.get_pos()
        self.keys = pygame.key.get_pressed()
        if not self.buttonList[self.button_tutorial][1]:
            self.keyPressed()
            self.mouseMotion(surface)
            self.timerFired(time)
        for event in pygame.event.get():
            # not in tutorial mode
            if not self.buttonList[self.button_tutorial][1]:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button in [4, 5]:
                    self.mouseScroll(*(event.pos), event.button)
                            
                elif event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
                    self.mouseDrag(*(event.pos))
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mousePressed(*(event.pos), surface)
            #  quitting
            elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
    
    def graphicsUpdate(self, surface):
        if self.buttonList[self.button_tutorial][1]:
            surface.blit(self.screen_tutorial, (0, 0))
        else:
            self.grid.wireFrame(surface)
            
            for s in solids:
                s.wireFrame(surface)
            
            self.axis.display(surface)
            self.panel.draw(surface)

    
    def run(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.initGui()

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


import pygame
import tkinter as tk
import sys, math, json, datetime
from tkinter.filedialog import askopenfilename, asksaveasfilename


from gui import *
from display import *
from card import *

"""
move back and forth: q, e
move up and down: w, s
move left and right: a, d
zoom: mouse scroll
rotate: mouse drag

"""

GRAY = (235, 235, 235)
BLACK = (0, 0, 0)
LIGHTGRAY = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (100, 200, 239)
RED = (255, 110, 110)
ORANGE = (255, 220, 150)

solids = []
cards = []

# barebone from: https://qwewy.gitbooks.io/pygame-module-manual/content/chapter1/the-mainloop.html
class Main(object):
    def __init__(self, width = 1440, height = 840, fps=10):
        self.width = width
        self.height = height
        self.fps = fps
        self.bgColor = GRAY
        self.title = "Wire Frame 3D"

        self.grid = Grid(LIGHTGRAY, (0,0,0), 1, 5)
        #self.axis = Axis((BLUE, RED, GREEN))
        self.axis = Axis(((0,0,255), (0,255,255), (255,0,255)))
        
        pygame.init()

    def initGui(self, surface): 
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        # panel
        self.panelWidth = self.width / 4
        self.panel = Panel(self.panelWidth, self.height, ORANGE)
        
        # tutorial
        self.screen_tutorial = pygame.image.load('images/tutorial.png').convert_alpha()
        pygame.transform.scale(self.screen_tutorial, (self.width, self.height))
        
        # button
        icon_tutorialA =    pygame.image.load('images/tutorialA.png').convert_alpha()
        icon_tutorialD =    pygame.image.load('images/tutorialD.png').convert_alpha()
        icon_addA =         pygame.image.load('images/addA.png').convert_alpha()
        icon_addD =         pygame.image.load('images/addD.png').convert_alpha()
        icon_importA =      pygame.image.load('images/importA.png').convert_alpha()
        icon_importD =      pygame.image.load('images/importD.png').convert_alpha()

        icon_homeA =        pygame.image.load('images/homeA.png').convert_alpha()
        icon_homeD =        pygame.image.load('images/homeD.png').convert_alpha()
        icon_xyplaneA =     pygame.image.load('images/xyplaneA.png').convert_alpha()
        icon_xyplaneD =     pygame.image.load('images/xyplaneD.png').convert_alpha()
        icon_xzplaneA =     pygame.image.load('images/xzplaneA.png').convert_alpha()
        icon_xzplaneD =     pygame.image.load('images/xzplaneD.png').convert_alpha()
        icon_yzplaneA =     pygame.image.load('images/yzplaneA.png').convert_alpha()
        icon_yzplaneD =     pygame.image.load('images/yzplaneD.png').convert_alpha()
        icon_rotateA =      pygame.image.load('images/rotateA.png').convert_alpha()
        icon_rotateD =      pygame.image.load('images/rotateD.png').convert_alpha() 
        icon_perspectiveA = pygame.image.load('images/perspectiveA.png').convert_alpha()
        icon_perspectiveD = pygame.image.load('images/perspectiveD.png').convert_alpha()
        icon_axonometricA = pygame.image.load('images/axonometricA.png').convert_alpha()
        icon_axonometricD = pygame.image.load('images/axonometricD.png').convert_alpha()
        icon_screenshotA =  pygame.image.load('images/screenshotA.png').convert_alpha()
        icon_screenshotD =  pygame.image.load('images/screenshotD.png').convert_alpha()
        icon_exportA =      pygame.image.load('images/exportA.png').convert_alpha()
        icon_exportD =      pygame.image.load('images/exportD.png').convert_alpha()
        
        self.icon_confirmA =     pygame.image.load('images/confirmA.png').convert_alpha()
        self.icon_confirmD =     pygame.image.load('images/confirmD.png').convert_alpha()
        self.icon_cancelA =      pygame.image.load('images/cancelA.png').convert_alpha()
        self.icon_cancelD =      pygame.image.load('images/cancelD.png').convert_alpha()

        
        # top pf the panel
        self.buttonWidthP = self.width / 30
        self.button_tutorial =  Button(10, 20, self.buttonWidthP, self.buttonWidthP, icon_tutorialD, icon_tutorialA, "tutorial")
        self.button_add =       Button(self.panelWidth - self.buttonWidthP - 10, 20, self.buttonWidthP, self.buttonWidthP, icon_addD, icon_addA, "add object")
        self.button_import =    Button(self.panelWidth - 2 * self.buttonWidthP - 2 * 10, 20, self.buttonWidthP, self.buttonWidthP, icon_importD, icon_importA, "import")
        
        # bottom of screen
        self.buttonWidthW = self.width / 20
        c, d = self.width * 0.6, self.buttonWidthW * 1.2
        self.button_home =        Button(c - 4 * d, self.height - d, self.buttonWidthW, self.buttonWidthW, icon_homeD, icon_homeA, "home")
        self.button_xyplane =     Button(c - 3 * d, self.height - d, self.buttonWidthW, self.buttonWidthW, icon_xyplaneD, icon_xyplaneA, "look at xy plane")
        self.button_xzplane =     Button(c - 2 * d, self.height - d, self.buttonWidthW, self.buttonWidthW, icon_xzplaneD, icon_xzplaneA, "look at xz plane")
        self.button_yzplane =     Button(c - 1 * d, self.height - d, self.buttonWidthW, self.buttonWidthW, icon_yzplaneD, icon_yzplaneA, "look at yz plane")
        self.button_rotate =      Button(c - 0 * d, self.height - d, self.buttonWidthW, self.buttonWidthW, icon_rotateD, icon_rotateA, "auto rotate")    
        self.button_perspective = Button(c + 1 * d, self.height - d, self.buttonWidthW, self.buttonWidthW, icon_perspectiveD, icon_perspectiveA, "perspective")
        self.button_axonometric = Button(c + 1 * d, self.height - d, self.buttonWidthW, self.buttonWidthW, icon_axonometricD, icon_axonometricA, "axonometric")
        self.button_screenshot =  Button(c + 2 * d, self.height - d, self.buttonWidthW, self.buttonWidthW, icon_screenshotD, icon_screenshotA, "screenshot")    
        self.button_export =      Button(c + 3 * d, self.height - d, self.buttonWidthW, self.buttonWidthW, icon_exportD, icon_exportA, "export")
        


        # button: isDisplaying, isInMode
        self.buttonList = {
                            self.button_tutorial: [True, False],
                            self.button_add: [True, False],
                            self.button_import: [True, False],
                            self.button_home: [True, False],
                            self.button_xyplane: [True, False],
                            self.button_xzplane: [True, False],
                            self.button_yzplane: [True, False],
                            self.button_rotate: [True, False],
                            self.button_perspective: [False, True],
                            self.button_axonometric: [True, False],
                            self.button_screenshot: [True, False], 
                            self.button_export: [True, False],
                            }

        # scroll
        self.scroll_length = 3
        self.scroll_content = pygame.Surface((int(self.panelWidth), int(self.scroll_length)))
        self.scroll_content.fill(ORANGE)
        self.scroll = Scroll(0, 80, self.panelWidth, self.height - 80, self.scroll_content)

        # drop down menu
        options = ["Prism", "Pyramid", "Polyhedron", "Sphere", "3D Surface", "3D Curve", "Custom"]
        self.dropDownMenu = DropDownMenu(self.panelWidth - self.buttonWidthP - 10, 80, 200, 50, options)
        self.isDroppingDown = False

        # text entering
        self.textentering = False 
        self.currCard = None   


    def mousePressed(self, x, y, surface):
        if self.buttonList[self.button_tutorial][1]:
            self.buttonList[self.button_tutorial][1] = False

        if self.button_tutorial.isInBound(x, y):
            self.buttonList[self.button_tutorial][1] = True

        elif self.button_home.isInBound(x, y):
            cam.home(self.buttonList[self.button_perspective][1])
            self.buttonList[self.button_rotate][1] == 0

        elif self.button_xyplane.isInBound(x, y):
            cam.xyPlane(self.buttonList[self.button_perspective][1])
        elif self.button_xzplane.isInBound(x, y):
            cam.xzPlane(self.buttonList[self.button_perspective][1])
        elif self.button_yzplane.isInBound(x, y):
            cam.yzPlane(self.buttonList[self.button_perspective][1])

        elif self.button_rotate.isInBound(x, y):
            self.buttonList[self.button_rotate][1] = not self.buttonList[self.button_rotate][1]

        elif self.button_perspective.isInBound(x, y):
            self.buttonList[self.button_perspective][0] = not self.buttonList[self.button_perspective][0]
            self.buttonList[self.button_perspective][1] = not self.buttonList[self.button_perspective][1]
            self.buttonList[self.button_axonometric][0] = not self.buttonList[self.button_axonometric][0]
            self.buttonList[self.button_axonometric][1] = not self.buttonList[self.button_axonometric][1]
            cam.home(self.buttonList[self.button_perspective][1])

        elif self.button_screenshot.isInBound(x, y):
            #filename = asksaveasfilename(initialdir = "/", defaultextension= ".jpg",
            #                                initialfile="screenshot " + str(datetime.datetime.now()))
            filename = "screenshot " + str(datetime.datetime.now()) + ".jpg"
            if filename is not None:
                pygame.image.save(surface, filename)

        elif self.button_export.isInBound(x,y):
            #filename = asksaveasfilename(initialdir = "/", defaultextension= ".txt",
                                            #initialfile="data " + str(datetime.datetime.now()))
            filename = "data " + str(datetime.datetime.now()) + ".txt"
            if filename is not None:
                with open(filename, 'w') as outfile:  
                    for o in solids:
                        json.dump(o.__dict__, outfile)

        elif self.button_add.isInBound(x, y):
            self.isDroppingDown = not self.isDroppingDown
        
        elif self.isDroppingDown:
            self.isDroppingDown = False
            selection = self.dropDownMenu.isInBound(x, y)
            if selection == 0:
                c = PrismCard(self.panelWidth, cards, self.icon_confirmD, self.icon_confirmA, self.icon_cancelD, self.icon_cancelA)
                cards.append(c)
                self.scroll_length = c.getBottom()
                self.scroll_content = pygame.Surface((int(self.panelWidth), int(self.scroll_length)))
                self.scroll_content.fill(ORANGE)
                self.scroll = Scroll(0, 80, self.panelWidth, self.height - 80, self.scroll_content)
                
            elif selection == 1:
                c = PyramidCard(self.panelWidth, cards, self.icon_confirmD, self.icon_confirmA, self.icon_cancelD, self.icon_cancelA)
                cards.append(c)
                self.scroll_length = c.getBottom()
                self.scroll_content = pygame.Surface((int(self.panelWidth), int(self.scroll_length)))
                self.scroll_content.fill(ORANGE)
                self.scroll = Scroll(0, 80, self.panelWidth, self.height - 80, self.scroll_content)
            
            elif selection == 2:
                c = PolyhedronCard(self.panelWidth, cards, self.icon_confirmD, self.icon_confirmA, self.icon_cancelD, self.icon_cancelA)
                cards.append(c)
                self.scroll_length = c.getBottom()
                self.scroll_content = pygame.Surface((int(self.panelWidth), int(self.scroll_length)))
                self.scroll_content.fill(ORANGE)
                self.scroll = Scroll(0, 80, self.panelWidth, self.height - 80, self.scroll_content)
            elif selection == 3:
                c = SphereCard(self.panelWidth, cards, self.icon_confirmD, self.icon_confirmA, self.icon_cancelD, self.icon_cancelA)
                cards.append(c)
                self.scroll_length = c.getBottom()
                self.scroll_content = pygame.Surface((int(self.panelWidth), int(self.scroll_length)))
                self.scroll_content.fill(ORANGE)
                self.scroll = Scroll(0, 80, self.panelWidth, self.height - 80, self.scroll_content)
            elif selection == 4:
                pass
            elif selection == 5:
                pass
            elif selection == 6:
                pass
            
            self.scroll.setDisplayY(cards[-1].getTop())
        else:
            poped = False
            for i in range(len(cards)):
                poped, self.textentering = cards[i].inputUpdate(self.scroll, x, y, solids, i)
                if poped:
                    cards.pop(i)
                    p = i
                    break
                elif self.textentering:
                    self.currCard = i
                    break

            if poped:
                if cards == []:
                    self.scroll_length = 3
                else:
                    for i in range(p, len(cards)):
                        cards[i].updateTop(cards, i)
                    self.scroll_length = cards[-1].getBottom()
                
                self.scroll_content = pygame.Surface((int(self.panelWidth), int(self.scroll_length)))
                self.scroll_content.fill(ORANGE)
                self.scroll = Scroll(0, 80, self.panelWidth, self.height - 80, self.scroll_content)

    def textEntry(self, events):
        if self.currCard != None and self.currCard < len(cards):
            cards[self.currCard].textUpdate(events)

    def mouseMotion(self, surface):
        x, y = self.pos
        for b in self.buttonList:
            if self.buttonList[b][0]: 
                b.isInBound(x, y)
                b.draw(surface)
        self.scroll.isInScrollBarY(x, y)
        self.dropDownMenu.isInBound(x, y)
        for i in range(len(cards)):
            cards[i].hovering(self.scroll, x, y)
    
    def mouseScroll(self, x, y, button):
        # not on the panel, zoom
        if x > self.panelWidth:
            if button == 4:
                cam.zoom(self.displacement)
            if button == 5:
                cam.zoom(-self.displacement)

        # in the scroll zone, scroll
        elif self.scroll.isInWindow(x, y):
            if button == 4:
                self.scroll.scrollY(-self.displacement * 250)
            elif button == 5:
                self.scroll.scrollY(self.displacement * 250)
            
    
    def mouseDrag(self, x, y):
        # not on the panel, rotate
        if x > self.panelWidth:
            angleXY, angleXZ = self.rel[0] / 200, self.rel[1] / 200
            cam.rotateXY(angleXY)
            cam.rotateXZ(angleXZ)

        # in scroll bar, drag to scroll
        self.scroll.dragY(x, y, self.rel[1])
        

    def keyPressed(self):
        if not self.textentering: 
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
        angle = self.displacement / 4
        if self.buttonList[self.button_rotate][1]:
            cam.rotateXY(angle)

    def eventsUpdate(self, surface, clock):
        time = clock.tick(self.fps)
        self.displacement = self.fps / 50
        self.rel = pygame.mouse.get_rel()
        self.pos = pygame.mouse.get_pos()
        self.keys = pygame.key.get_pressed()
        self.events = pygame.event.get()
        if not self.buttonList[self.button_tutorial][1]:
            self.mouseMotion(surface)
            self.timerFired(time)
            self.keyPressed()
            self.textEntry(self.events)
        
        for event in self.events:
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
            self.grid.wireFrame(surface, self.buttonList[self.button_perspective][1])
            
            for s in solids:
                s.wireFrame(surface, self.buttonList[self.button_perspective][1])

            
            self.axis.display(surface, self.buttonList[self.button_perspective][1])
            self.panel.draw(surface)
            self.scroll.draw(surface)
            
            for c in cards:
                c.draw(self.scroll_content)
            if self.isDroppingDown:
                self.dropDownMenu.draw(surface)
    
    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.initGui(screen)

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


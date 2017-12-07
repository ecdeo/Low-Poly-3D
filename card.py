from display import *
from gui import *
from textinput import *

class Card(object):
    def __init__(self, panelWidth, cardList, icon_confirmD, icon_confirmA, icon_cancelD, icon_cancelA):
        self.panelWidth = panelWidth
        self.buttonWidth = self.panelWidth / 8
        self.gap = 3
        self.textSize = 20
        self.font = "font/Ubuntu-L.ttf"
        self.TITLE = pygame.font.Font(self.font, 32)
        self.TEXT =  pygame.font.Font(self.font, self.textSize)

        self.cardList = cardList
        self.x = self.gap
        self.y = self.setTop(self.cardList)
        self.w = self.panelWidth - self.gap * 2
        self.h = 500
        self.icon_cancelA = icon_cancelA
        self.button_confirm =   Button(10, self.h - self.buttonWidth - 10, self.buttonWidth, self.buttonWidth, icon_confirmD, icon_confirmA)
        self.button_cancel =    Button(self.panelWidth - self.buttonWidth - 10, self.h - self.buttonWidth - 10, self.buttonWidth, self.buttonWidth, icon_cancelD, icon_cancelA)
        
        self.textList = []
        
        self.R = TextInput(self.font, self.textSize)
        self.G = TextInput(self.font, self.textSize)
        self.B = TextInput(self.font, self.textSize)
        self.CX = TextInput(self.font, self.textSize)
        self.CY = TextInput(self.font, self.textSize)
        self.CZ = TextInput(self.font, self.textSize)
        
        self.s = 80
        self.firstRow = 50
        self.Rb = TextEntryBox(self.s, self.firstRow, 20, self.textSize, "R")
        self.Gb = TextEntryBox(self.s + 60, self.firstRow, 20, self.textSize, "G")
        self.Bb = TextEntryBox(self.s + 120, self.firstRow, 20, self.textSize, "B")

        self.secondRow = 80
        self.CXb = TextEntryBox(self.s, self.secondRow, 20, self.textSize, "0")
        self.CYb = TextEntryBox(self.s + 60, self.secondRow, 20, self.textSize, "0")
        self.CZb = TextEntryBox(self.s + 120, self.secondRow, 20, self.textSize, "0")
        self.thirdRow = 110
        self.fourthRow = 140
        self.fifthRow = 170
        
    
    def setTop(self, cardList):
        if cardList == []:
            y = self.gap
        else:
            y = self.cardList[-1].getBottom() 
        return y
    
    def updateTop(self, cardList, i):
        if i - 1 <= 0:
            self.y = 3
        else:
            self.y = self.cardList[i-1].getBottom()
    def getBottom(self):
        return self.y + self.h + self.gap
    def getTop(self):
        return self.y
    def hovering(self, scroll, x, y):
        y = y + scroll.getDisplayY() - 80 - self.y 
        self.button_confirm.isInBound(x, y)
        self.button_cancel.isInBound(x, y)

    def inputUpdate(self, scroll, px, py, solidList, i):
        py = py + scroll.getDisplayY() - 80 - self.y 
        if self.button_confirm.isInBound(px, py):
            if i >= len(solidList):
                solidList.append(self.solid)
            else: 
                solidList[i] = self.solid

        elif self.button_cancel.isInBound(px, py):
            if i >= len(solidList):
                pass
            else: 
                solidList.pop(i)
            return True

    def textUpdate(self, events):
        if self.currField != None:
            self.textList[self.currField].update(events)
            self.modifySolid()
    
    def draw(self, surface):
        #self.card = pygame.Surface((self.w,self.h))
        #self.card.fill((255,255,255))
        
        self.title = self.TITLE.render(type(self).__name__[:-4], True, (0,0,0), (255,255,255))
        self.card.blit(self.title, (0, 0))
        
        self.color = self.TEXT.render("Color", True, (0,0,0), (255,255,255))
        self.card.blit(self.color, (0, self.firstRow))

        self.center = self.TEXT.render("Center", True, (0,0,0), (255,255,255))
        self.card.blit(self.center, (0, self.secondRow))


        self.button_confirm.draw(self.card)
        self.button_cancel.draw(self.card)

        for i in range(0, len(self.textList), 2):
            self.textList[i + 1].draw(self.card)
            self.card.blit(self.textList[i].get_surface(), self.textList[i + 1].getBounds())

        surface.blit(self.card, (int(self.x), int(self.y)))

    def modifySolid(self):
        if self.currField == 0:
            n = self.R.get_text()
            if n != "":
                if isinstance(eval(n), int) and eval(n) <= 255 and eval(n) >= 0:
                    self.solid.changeR(eval(n))
                else:
                    self.textList[self.currField + 1].isLegal(False)
        
        elif self.currField == 2:
            n = self.G.get_text()
            if n != "":
                if isinstance(eval(n), int) and eval(n) <= 255 and eval(n) >= 0:
                    self.solid.changeG(eval(n))
                else:
                    self.textList[self.currField + 1].isLegal(False)
        elif self.currField == 4:
            n = self.B.get_text()
            if n != "":
                if isinstance(eval(n), int) and eval(n) <= 255 and eval(n) >= 0:
                    self.solid.changeB(eval(n))
                else:
                    self.textList[self.currField + 1].isLegal(False)
        elif self.currField == 6:
            n = self.CX.get_text()
            if n != "":
                if isinstance(eval(n), (int, float)) and eval(n) <= 100 and eval(n) >= 0:
                    self.solid.changeCX(eval(n))
                else:
                    self.textList[self.currField + 1].isLegal(False)
        elif self.currField == 8:
            n = self.CY.get_text()
            if n != "":
                if isinstance(eval(n), (int, float)) and eval(n) <= 100 and eval(n) >= 0:
                    self.solid.changeCY(eval(n))
                else:
                    self.textList[self.currField + 1].isLegal(False)
        elif self.currField == 10:
            n = self.CZ.get_text()
            if n != "":
                if isinstance(eval(n), (int, float)) and eval(n) <= 100 and eval(n) >= 0:
                    self.solid.changeCZ(eval(n))
                else:
                    self.textList[self.currField].isLegal(False)

class PrismCard(Card):
    def __init__(self, panelWidth, cardList, icon_confirmD, icon_confirmA, icon_cancelD, icon_cancelA):
        super().__init__(panelWidth, cardList, icon_confirmD, icon_confirmA, icon_cancelD, icon_cancelA)
        self.solid = Prism()

        self.Sides = TextInput(self.font, self.textSize)
        self.SideLen = TextInput(self.font, self.textSize)
        self.Height = TextInput(self.font, self.textSize)
        
        
        self.Sidesb = TextEntryBox(160, self.thirdRow, 20, self.textSize, "3")
        self.SideLenb = TextEntryBox(160, self.fourthRow, 20, self.textSize, "1")
        self.Heightb = TextEntryBox(160, self.fifthRow, 20, self.textSize, "1")

        self.textList = [self.R, self.Rb, self.G, self.Gb, self.B, self.Bb,
                        self.CX, self.CXb, self.CY, self.CYb, self.CZ, self.CZb, 
                        self.Sides, self.Sidesb, self.SideLen, self.SideLenb, self.Height, self.Heightb]
        
    def draw(self, surface):
        self.card = pygame.Surface((self.w, self.h))
        self.card.fill((255,255,255))
        self.sides = self.TEXT.render("number of sides", True, (0,0,0), (255,255,255))
        self.card.blit(self.sides, (0, self.thirdRow))
        self.sidelen = self.TEXT.render("side length", True, (0,0,0), (255,255,255))
        self.card.blit(self.sidelen, (0, self.fourthRow))
        self.hei = self.TEXT.render("height", True, (0,0,0), (255,255,255))
        self.card.blit(self.hei, (0, self.fifthRow))
        super().draw(surface)


    def inputUpdate(self, scroll, px, py, solidList, i):
        result = super().inputUpdate(scroll, px, py, solidList, i)
        py = py + scroll.getDisplayY() - 80 - self.y 
        for i in range(0, len(self.textList), 2):
            textentering = self.textList[i + 1].isInBound(px, py)
            if textentering:
                self.currField = i
                break
            self.currField = None
        return result, textentering

    def modifySolid(self):
        super().modifySolid()


        """
        numSides > 0
        """


class PyramidCard(Card):
    def __init__(self, panelWidth, cardList, icon_confirmD, icon_confirmA, icon_cancelD, icon_cancelA):
        super().__init__(panelWidth, cardList, icon_confirmD, icon_confirmA, icon_cancelD, icon_cancelA)
        self.s = Pyramid()
    
    def draw(self, surface):
        self.card = pygame.Surface((self.w, self.h))
        self.card.fill((255,255,255))
        super().draw(surface)

    def inputUpdate(self, scroll, px, py, solidList, i):
        result = super().inputUpdate(scroll, px, py, solidList, i)
        py = py + scroll.getDisplayY() - 80 - self.y 
        for i in range(0, len(self.textList), 2):
            textentering = self.textList[i + 1].isInBound(px, py)
            if textentering:
                self.currField = i
                break
        return result, textentering

    def modifySolid(self):
        pass

class PolyhedronCard(Card):
    def __init__(self, panelWidth, cardList, icon_confirmD, icon_confirmA, icon_cancelD, icon_cancelA):
        super().__init__(panelWidth, cardList, icon_confirmD, icon_confirmA, icon_cancelD, icon_cancelA)
        self.s = Polyhedron()
    
    def draw(self, surface):
        self.card = pygame.Surface((self.w, self.h))
        self.card.fill((255,255,255))
        super().draw(surface)

    def inputUpdate(self, scroll, px, py, solidList, i):
        result = super().inputUpdate(scroll, px, py, solidList, i)
        py = py + scroll.getDisplayY() - 80 - self.y 
        for i in range(0, len(self.textList), 2):
            textentering = self.textList[i + 1].isInBound(px, py)
            if textentering:
                self.currField = i
                break
        return result, textentering

    def modifySolid(self):
        pass

class SphereCard(Card):
    def __init__(self, panelWidth, cardList, icon_confirmD, icon_confirmA, icon_cancelD, icon_cancelA):
        super().__init__(panelWidth, cardList, icon_confirmD, icon_confirmA, icon_cancelD, icon_cancelA)
        self.s = Sphere()
    
    def draw(self, surface):
        self.card = pygame.Surface((self.w, self.h))
        self.card.fill((255,255,255))
        super().draw(surface)

    def inputUpdate(self, scroll, px, py, solidList, i):
        result = super().inputUpdate(scroll, px, py, solidList, i)
        py = py + scroll.getDisplayY() - 80 - self.y 
        for i in range(0, len(self.textList), 2):
            textentering = self.textList[i + 1].isInBound(px, py)
            if textentering:
                self.currField = i
                break
        return result, textentering

    def modifySolid(self):
        pass

    """
    numLatitude, numlongitute > 0
    """

class Surface3DCard(Card):
    pass

class Curve3DCard(Card):
    pass

class Custom(Card):
    pass
        
from display import *
from gui import *
from textinput import *

class Card(object):
    def __init__(self, panelWidth, cardList, icon_confirmD, icon_confirmA, icon_cancelD, icon_cancelA):
        self.panelWidth = panelWidth
        self.buttonWidth = self.panelWidth / 8
        self.gap = 3
        self.textSize = 16
        self.font = "font/Ubuntu-L.ttf"
        self.TITLE = pygame.font.Font(self.font, 32)
        self.TEXT =  pygame.font.Font(self.font, 16)

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
    
        self.Rb = TextEntryBox(40, 50, 10, 16, "R")
        self.textList = [self.R, self.Rb]
    
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
                solidList.append(self.s)
            else: 
                solidList[i] = self.s

        elif self.button_cancel.isInBound(px, py):
            if i >= len(solidList):
                pass
            else: 
                solidList.pop(i)
            return True

    def draw(self, surface):
        #self.card = pygame.Surface((self.w,self.h))
        #self.card.fill((255,255,255))
        
        self.title = self.TITLE.render(type(self).__name__[:-4], True, (0,0,0), (255,255,255))
        self.card.blit(self.title, (0, 0))
        
        self.color = self.TEXT.render("Color", True, (0,0,0), (255,255,255))
        self.card.blit(self.color, (0, 40))

        self.button_confirm.draw(self.card)
        self.button_cancel.draw(self.card)

        for i in range(0, len(self.textList), 2):
            self.textList[i + 1].draw(self.card)
            self.card.blit(self.textList[i].get_surface(), self.textList[i + 1].getBounds())

        surface.blit(self.card, (int(self.x), int(self.y)))

class PrismCard(Card):
    def __init__(self, panelWidth, cardList, icon_confirmD, icon_confirmA, icon_cancelD, icon_cancelA):
        super().__init__(panelWidth, cardList, icon_confirmD, icon_confirmA, icon_cancelD, icon_cancelA)
        self.s = Prism()
        
    def draw(self, surface):
        self.card = pygame.Surface((self.w, self.h))
        self.card.fill((255,255,255))
        super().draw(surface)


    def inputUpdate(self, scroll, px, py, solidList, i):
        result = super().inputUpdate(scroll, px, py, solidList, i)
        




        return result




    def modifySolid(self):
        pass
        """
        numSides > 0
        """


class PyramidCard(Card):
    def __init__(self, panelWidth, cardList, icon_confirmD, icon_confirmA, icon_cancelD, icon_cancelA):
        super().__init__(panelWidth, cardList, icon_confirmD, icon_confirmA, icon_cancelD, icon_cancelA)
        self.s = Pyramid()
    
    def draw(self, surface):
        super().draw(surface)



        surface.blit(self.card, (int(self.x), int(self.y)))

    def inputUpdate(self, scroll, px, py, solidList, i):
        result = super().inputUpdate(scroll, px, py, solidList, i)
        return result


    def modifySolid(self):
        pass

class PolyhedronCard(Card):
    def __init__(self, panelWidth, cardList, icon_confirmD, icon_confirmA, icon_cancelD, icon_cancelA):
        super().__init__(panelWidth, cardList, icon_confirmD, icon_confirmA, icon_cancelD, icon_cancelA)
        self.s = Polyhedron()
    
    def draw(self, surface):
        super().draw(surface)



        surface.blit(self.card, (int(self.x), int(self.y)))

    def inputUpdate(self, scroll, px, py, solidList, i):
        result = super().inputUpdate(scroll, px, py, solidList, i)
        return result



    def modifySolid(self):
        pass

class SphereCard(Card):
    def __init__(self, panelWidth, cardList, icon_confirmD, icon_confirmA, icon_cancelD, icon_cancelA):
        super().__init__(panelWidth, cardList, icon_confirmD, icon_confirmA, icon_cancelD, icon_cancelA)
        self.s = Sphere()
    
    def draw(self, surface):
        super().draw(surface)



        surface.blit(self.card, (int(self.x), int(self.y)))

    def inputUpdate(self, scroll, px, py, solidList, i):
        result = super().inputUpdate(scroll, px, py, solidList, i)
        return result



    def modifySolid(self):
        pass

    """
    numLatitude, numlongitute > 0
    """

class Surface3DCard(Card):
    def __init__(self, arg):
        super().__init__()
        self.arg = arg

class Curve3DCard(Card):
    pass

class Custom(Card):
    pass
        
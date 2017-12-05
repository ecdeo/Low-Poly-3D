import pygame
import sys, math

class Panel(object):
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (0, 0, self.width, self.height))

class Button(object):
    # x0, y0: the upper left corner
    def __init__(self, x0, y0, width, height, patternD, patternA, label = "", labelColor = (0,0,0)):
        self.x0 = x0
        self.y0 = y0
        self.width = width
        self.height = height
        w, h = patternD.get_size()
        self.patternD = pygame.transform.scale(patternD, (int(self.width), int(self.height)))
        self.patternA = pygame.transform.scale(patternA, (int(self.width), int(self.height)))
        
        self.label = label
        self.labelColor = labelColor

        self.active = False
    
    def isInBound(self, x, y):
        result =  min(max(x, self.x0), self.x0 + self.width) == x and min(max(y, self.y0), self.y0 + self.height) == y
        if result:
            self.active = True
        else:
            self.active = False
        return result

    def draw(self, surface):
        labelSize = surface.get_height() / 50
        if self.active:
            surface.blit(self.patternA, (self.x0, self.y0))
            
            font = pygame.font.Font("font/Ubuntu-L.ttf", int(labelSize))
            label = font.render(self.label, True, self.labelColor)
            w, h = label.get_size()
            surface.blit(label,(self.x0 + self.width / 2 - w / 2, int(self.y0 - h)))
        
        else:
            surface.blit(self.patternD, (self.x0, self.y0))

    def getHashable(self):
        return (self.x0, self.y0, self.width, self.height, self.patternA, self.patternD)

    def __hash__(self):
        return hash(self.getHashable())

    def __eq__(self, other):
        return isinstance(other, Button) and self.getHashable() == other.getHashable()

class TextInput(object):
    pass
    
class Scroll(object):
    # content: a surface of the content
    def __init__(self, x0, y0, windowWidth, windowHeight, content, color = [(130, 130, 130), (200, 200, 200)]):
        self.x0 = x0
        self.y0 = y0
        self.winWidth = windowWidth
        self.winHeight = windowHeight
        self.content = content
        self.conWidth, self.conHeight = content.get_size()
        self.color = color
        self.barColor = color[0]
        self.barWidth = 8
        # in display
        self.displayX = 0
        self.displayY = 0
    
    def isInWindow(self, x, y):
        return min(max(x, self.x0), self.x0 + self.winWidth) == x and min(max(y, self.y0), self.y0 + self.winHeight) == y
    
    def scrollX(self, displacement):
        self.displayX += displacement
        if self.displayX < 0:
            self.displayX = 0
        elif self.displayX > self.conWidth - self.winWidth:
            self.displayX = self.conWidth - self.winWidth

    def scrollY(self, displacement):
        self.displayY += displacement
        if self.displayY < 0:
            self.displayY = 0
        elif self.displayY > self.conHeight - self.winHeight:
            self.displayY = self.conHeight - self.winHeight
    
    def isInScrollBarX(self, x, y):
        result = min(max(x, self.startX), self.startX + self.lengthX) == x and min(max(y, self.y0 + self.winHeight - self.barWidth), self.y0 + self.winHeight) == y
        if result:
            self.barColor = self.color[1]
        else:
            self.barColor = self.color[0]
        return result

    def isInScrollBarY(self, x, y):
        result = min(max(x, self.x0 + self.winWidth - self.barWidth), self.x0 + self.winWidth) == x and min(max(y, self.startY), self.startY + self.lengthY) == y
        if result:
            self.barColor = self.color[1]
        else:
            self.barColor = self.color[0]
        return result
    
    def dragX(self, x, y, displacement):
        if self.isInScrollBarX(x, y):
            self.scrollX(displacement * self.conWidth / self.winWidth)
    
    def dragY(self, x, y, displacement):
        if self.isInScrollBarY(x, y):
            self.scrollY(displacement * self.conHeight / self.winHeight)

    def scrollBarX(self, surface):
        self.lengthX = self.winWidth * self.conWidth / self.winWidth
        self.startX = self.x0 + self.winWidth * self.displayX / self.conWidth
        if self.conWidth <= self.winWidth:
            pass
        else:
            pygame.draw.rect(surface, self.barColor, (self.startX, self.y0 + self.winHeight - self.barWidth, self.lengthX, self.barWidth))

    def scrollBarY(self, surface):
        self.lengthY = self.winHeight * self.winHeight / self.conHeight
        self.startY = self.y0 + self.winHeight * self.displayY / self.conHeight
        if self.conHeight <= self.winHeight:
            pass
        else:
            pygame.draw.rect(surface, self.barColor, (self.x0 + self.winWidth - self.barWidth, self.startY, self.barWidth, self.lengthY))

    def contentInDisplay(self, surface):
        surface.blit(self.content, (self.x0, self.y0), (self.displayX, self.displayY, self.winWidth, self.winHeight))
    
    def draw(self, surface):
        self.contentInDisplay(surface)
        self.scrollBarX(surface)
        self.scrollBarY(surface)
        


class DropDownMenu(object):
    pass
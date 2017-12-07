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
    def __init__(self, x0, y0, width, height, patternD, patternA, label = "", labelFont = "font/Ubuntu-L.ttf", labelSize = 20, labelColor = (0,0,0)):
        self.x0 = x0
        self.y0 = y0
        self.width = width
        self.height = height
        w, h = patternD.get_size()
        self.patternD = pygame.transform.scale(patternD, (int(self.width), int(self.height)))
        self.patternA = pygame.transform.scale(patternA, (int(self.width), int(self.height)))
        
        self.label = label
        self.labelFont = labelFont
        self.labelSize = labelSize
        self.labelColor = labelColor
        self.font = pygame.font.Font(self.labelFont, self.labelSize)

        self.active = False
    
    def isInBound(self, x, y):
        result =  min(max(x, self.x0), self.x0 + self.width) == x and min(max(y, self.y0), self.y0 + self.height) == y
        if result:
            self.active = True
        else:
            self.active = False
        return result

    def draw(self, surface):
        if self.active:
            surface.blit(self.patternA, (self.x0, self.y0))
            
            label = self.font.render(self.label, True, self.labelColor)
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
    
class Scroll(object):
    # content: a surface of the content
    def __init__(self, x0, y0, windowWidth, windowHeight, content, color = [(160, 160, 160, 128), (200, 200, 200, 128)]):
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
    
    def getDisplayX(self):
        return self.displayX
    
    def getDisplayY(self):
        return self.displayY

    def setDisplayX(self, x):
        if self.conWidth <= self.winWidth:
            self.displayX = 0
        else:
            self.displayX = min(max(x, 0), self.conWidth - self.winWidth)
    
    def setDisplayY(self, y):
        if self.conHeight <= self.winHeight:
            self.displayY = 0
        else:
            self.displayY = min(max(y, 0), self.conHeight - self.winHeight)
    
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
            scrollBarX = pygame.Surface((int(self.lengthX), int(self.barWidth)), pygame.SRCALPHA)
            scrollBarX.fill(self.barColor)
            surface.blit(scrollBarX, (self.startX, self.y0 + self.winHeight - self.barWidth, self.lengthX, self.barWidth))

    def scrollBarY(self, surface):
        self.lengthY = self.winHeight * self.winHeight / self.conHeight
        self.startY = self.y0 + self.winHeight * self.displayY / self.conHeight
        if self.conHeight <= self.winHeight:
            pass
        else:
            scrollBarY = pygame.Surface((int(self.barWidth), int(self.lengthY)), pygame.SRCALPHA)
            scrollBarY.fill(self.barColor)
            surface.blit(scrollBarY, (self.x0 + self.winWidth - self.barWidth, self.startY, self.barWidth, self.lengthY))

    def contentInDisplay(self, surface):
        surface.blit(self.content, (self.x0, self.y0), (self.displayX, self.displayY, self.winWidth, self.winHeight))
    
    def draw(self, surface):
        self.contentInDisplay(surface)
        self.scrollBarX(surface)
        self.scrollBarY(surface)
        
class DropDownMenu(object):
    # options: list of options in str
    def __init__(self, x0, y0, width, optionHeight, options, textColor = (0, 0, 0), bgColor = [(255, 255, 255), (200, 200, 200)], textFont = "font/Ubuntu-L.ttf", textSize = 20):
        self.x0 = x0
        self.y0 = y0
        self.width = width
        self.optionHeight = optionHeight
        self.optionList = options
        self.number = len(options)
        self.isActive = [False] * self.number
        self.textColor = textColor
        self.bgColor = bgColor
        self.textFont = textFont
        self.textSize = textSize
        self.font = pygame.font.Font(self.textFont, self.textSize)
    def isInBound(self, x, y):
        selected = None
        for i in range(self.number):
            result =  min(max(x, self.x0), self.x0 + self.width) == x and min(max(y, self.y0 + i * self.optionHeight), self.y0 + (i + 1) * self.optionHeight) == y
            if result:
                self.isActive[i] = True
                selected = i
            else:
                self.isActive[i] = False
        return selected
    def draw(self, surface):
        for i in range(self.number):
            if self.isActive[i]:
                pygame.draw.rect(surface, self.bgColor[1], (self.x0, self.y0 + i * self.optionHeight, self.width, self.optionHeight))
            else:
                pygame.draw.rect(surface, self.bgColor[0], (self.x0, self.y0 + i * self.optionHeight, self.width, self.optionHeight))
            label = self.font.render(self.optionList[i], True, self.textColor, self.bgColor)
            w, h = label.get_size()
            surface.blit(label,(self.x0 + 5, int(self.y0 + i * self.optionHeight + self.optionHeight / 2 - h / 2)))

#class TextInput(object):
    #pass
class TextEntryBox(object):
    def __init__(self, x, y, w, h, initialText = ""):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.initialText = initialText
        self.color = (255, 255, 255)
        self.empty = True
        self.textSize = 16
        self.font = "font/Ubuntu-L.ttf"

    def isInBound(self, x, y, textentering):
        result = min(max(x, self.x), self.x + self.win) == x and min(max(y, self.y), self.y + self.w) == y
        if result:
            textentering = True
            self.empty = False
            self.color = (0, 255, 255)
        else:
            textentering = False
            self.color = (255, 255, 255)
        return textentering, result

    def isIllegal(self, legal):
        if legal:
            self.color = (255, 255, 255)
        else:
            self.color = (255, 255, 255)
    def draw(self, surface):
        if self.empty:
            self.TEXT =  pygame.font.Font(self.font, 16)
            self.TEXT.render(self.initialText, True, (200,200,200), (255,255,255))
        pygame.draw.line(surface, self.color, (self.x + self.h, self.y), (self.x + self.h, self.y + self.w), 1)
    def getBounds(self):
        return self.x, self.y, self.w, self.h




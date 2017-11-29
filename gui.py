import pygame, pygame.gfxdraw
import sys, math

class GUI(object):
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color

class Panel(GUI):
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color
    def draw(self, surface):
        pygame.gfxdraw.box(surface, (0, 0, self.width, self.height), self.color)

class Button(GUI):
    # x0, y0: the upper left corner
    def __init__(self, x0, y0, width, height, patternD, patternA):
        self.x0 = x0
        self.y0 = y0
        self.width = width
        self.height = height
        self.patternD = pygame.transform.scale(patternD, (int(width), int(height)))
        self.patternA = pygame.transform.scale(patternA, (int(width), int(height)))
    def isInBound(self, x, y):
        return min(max(x, self.x0), self.x0 + self.width) == x and min(max(y, self.y0), self.y0 + self.width) == y
    def drawD(self, surface):
        surface.blit(self.patternD, (self.x0, self.y0))
    def drawA(self, surface):
        surface.blit(self.patternA, (self.x0, self.y0))
    def getHashable(self):
        return (self.x0, self.y0, self.width, self.height, self.patternA, self.patternD)
    def __hash__(self):
        return hash(self.getHashable())
    def __eq__(self, other):
        return isinstance(other, Button) and self.getHashable() == other.getHashable()

class TextInput(GUI):
    pass
    
class Scroll(GUI):
    pass

class DropDownMenu(GUI):
    pass
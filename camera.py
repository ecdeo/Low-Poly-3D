import pygame, pygame.gfxdraw
import sys, math

class Cam(object):
    # position: tuple of camera position (x, y, z)
    # rotation: angle of rotation on XY plane and XZ plane
    def __init__(self, position = (8, 2, 10), rotation = (-0.2,-1)):
        self.position = list(position)
        self.rotation = list(rotation)
    
    def home(self):
        self.position = list((8, 2, 10))
        self.rotation = list((-0.2,-1))
    def zoom(self, displacement):
        self.position[0] += displacement
        self.position[1] += displacement
        self.position[2] += displacement
        
    def forthBack(self, displacement):
        self.position[0] += displacement

    def leftRight(self, displacement):
        self.position[1] += displacement

    def upDown(self, displacement):
        self.position[2] += displacement

    def rotateXY(self, angleXY):
        self.rotation[0] -= angleXY
    
    def rotateXZ(self, angleXZ):
        self.rotation[1] -= angleXZ

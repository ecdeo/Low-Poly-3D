import pygame, pygame.gfxdraw
import sys, math


CamDefault = [(10, 2, 1), (-0.3, -0.3)]
class Cam(object):
    # position: tuple of camera position (x, y, z)
    # rotation: angle of rotation on XY plane and XZ plane
    def __init__(self, position = CamDefault[0], rotation = CamDefault[1]):
        self.position = list(position)
        self.rotation = list(rotation)
    
    def home(self):
        self.position = list(CamDefault[0])
        self.rotation = list(CamDefault[1])
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

    def rotate(self, angle):
        self.rotateXY(angle)
        self.rotateXZ(angle)
    
    def rotateXY(self, angleXY):
        self.rotation[0] -= angleXY
    
    def rotateXZ(self, angleXZ):
        self.rotation[1] -= angleXZ

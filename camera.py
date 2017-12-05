import pygame
import sys, math


CamDefaultA = [(5, 1, 6), (-0.7, 0.5)]
CamDefaultP = [(10, 2, 1), (-0.3, -0.3)]
class Cam(object):
    # position: tuple of camera position (x, y, z)
    # rotation: angle of rotation on XY plane and XZ plane
    def __init__(self, position = CamDefaultP[0], rotation = CamDefaultP[1]):
        self.position = list(position)
        self.rotation = list(rotation)
        self.zoomFactor = 1
    
    def home(self, perspective):
        if perspective:
            self.position = list(CamDefaultP[0])
            self.rotation = list(CamDefaultP[1])
        else:
            self.position = list(CamDefaultA[0])
            self.rotation = list(CamDefaultA[1])
    def zoom(self, displacement = 0):
        self.zoomFactor = max(self.zoomFactor + displacement, 0)
        return self.zoomFactor
        
    def forthBack(self, displacement):
        self.position[0] += displacement

    def leftRight(self, displacement):
        self.position[1] -= displacement

    def upDown(self, displacement):
        self.position[2] += displacement

    def rotate(self, angle):
        self.rotateXY(angle)
        self.rotateXZ(angle)
    
    def rotateXY(self, angleXY):
        self.rotation[0] += angleXY
    
    def rotateXZ(self, angleXZ):
        self.rotation[1] -= angleXZ

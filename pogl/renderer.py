import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Renderer():
    def __init__(self):
        glutInit(sys.argv)
        print('Hi')

    def showImage(self, image):
        display = (image.shape[0], image.shape[1])
        pass


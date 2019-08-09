import cv2
import numpy as np

class OpenCVDrawer():

    def __init__(self):
        self.trackPoints = []
        self.image = []
        self.axis = []
        self._camera = []
        self._dist = []
        self.carInit = False



    def setParams(self, axis, _camera, _dist):
        self.axis = axis
        self._camera = _camera
        self._dist = _dist

    def setTrackPoints(self, trackPoints):
        self.trackPoints = trackPoints

    def setImage(self, image):
        self.image = image

    def getImage(self):
        return self.image

    def drawLine(self, start, finish, color=(0, 255, 0)):
        self.image = cv2.line(self.image, start, finish, color, 5)
        pass

    def drawTrack(self, number_of_markers):
        track = self.trackPoints.getTrack()

        for i in range(number_of_markers):
            if i == number_of_markers-1:
                self.drawLine(tuple((track[i][0])),
                              tuple(track[0][0]), color=(0, 127, 127))
            else:
                self.drawLine(tuple((track[i][0])),
                              tuple(track[i+1][0]), color=(0, 127, 127))

    def drawCar(self):
        if not self.carInit:
            self.image = cv2.circle(self.image, tuple(self.trackPoints.getTrack()[0][0]), 10, (255, 0, 0), 3)
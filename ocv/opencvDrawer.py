import cv2
import numpy as np

class OpenCVDrawer:

    def __init__(self, _camera, _dist):
        self.trackPoints = []
        self.image = []
        self.axis = []
        self._camera = _camera
        self._dist = _dist

    def setAxisImage(self, axis, image):
        self.axis = axis
        self.image = image

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

        for i in range(len(track)):
            if i == len(track)-1:
                h = track[i]
                self.drawLine(tuple((track[i]['position'])),
                              tuple(track[0]['position']), color=(0, 127, 127))
            else:
                h = track[i]
                self.drawLine(tuple((track[i]['position'])),
                              tuple(track[i+1]['position']), color=(0, 127, 127))

    def drawCar(self, car):
        print(car)
        self.image = cv2.circle(self.image, tuple(car), 10, (255, 0, 0), 3)
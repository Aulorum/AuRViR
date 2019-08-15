import cv2
import numpy as np

class OpenCVDrawer:

    def __init__(self, _camera, _dist, detector):
        self.trackPoints = []
        self.image = []
        self.axis = []
        self._camera = _camera
        self._dist = _dist
        self.detector = detector

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
        h = np.array([start, finish])
        self.image = cv2.polylines(self.image, [h], True, color, 4)
        pass

    def drawTrack(self):
        track = self.trackPoints.getTrack()
        if len(track) < 100:
            print(len(track))
        for i in range(len(track)):
            if i == len(track)-1:
                self.drawLine(track[i]['position'],
                              track[0]['position'], color=(180, 105, 255))
            else:
                self.drawLine(track[i]['position'],
                              track[i+1]['position'], color=(180, 105, 255))

    def drawCar(self, car):
        try:
            self.image = cv2.circle(self.image, tuple(car), 10, (255, 0, 0), 3)
        except: pass
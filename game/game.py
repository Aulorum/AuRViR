import cv2

from game.car import Car
from game.trackPoints import TrackPoints


class Game:

    def __init__(self, _camera, _dist):
        self.car = Car()
        self.time = 0
        self.trackPoints = TrackPoints(_camera, _dist)
        self.img = []
        self.imsize = []
        self.carInitialized = False
        pass

    def step(self):
        # Key "w" is opencv 119
        if cv2.waitKey(1) == 119:
            self.car.step(True)
            print('HI')
        else:
            self.car.step(False)
        pass

    def getCar(self):
        return self.car

    def getTrackPoints(self):
        return self.trackPoints

    def getCarPosition(self):
        try:
            part, pos = self.trackPoints.getPartForCar(self.car.getPosition())
            self.car.setPosition(pos)
            return part['position']
        except TypeError:
            self.car.setPosition(0)

    def setTPAxisAndMarker(self, axis, markers):
        self.trackPoints.setAxis(axis)
        self.trackPoints.setMarkers(markers)
        if not self.carInitialized:
            self.car.setPosition(0)
            self.carInitialized = True

    def setTPParams(self, _camera, _dist):
        self.trackPoints.setParams(_camera, _dist)

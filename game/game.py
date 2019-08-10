import keyboard
import cv2

from game.car import Car
from game.trackPoints import TrackPoints


class Game:

    def __init__(self, _camera, _dist, maxMarkerId):
        self.car = Car()
        self.time = 0
        self.trackPoints = TrackPoints(_camera, _dist, maxMarkerId)
        self.img = []
        self.imsize = []
        self.carInitialized = False
        pass

    def step(self):
        if keyboard.is_pressed('p'):
            self.car.step(True)
        else:
            self.car.step(False)
        pass

    def getCar(self):
        return self.car

    def getTrackPoints(self):
        return self.trackPoints

    def getCarPosition(self):
        part, pos = self.trackPoints.getPartForCar(self.car.getPosition())
        self.car.setPosition(pos)
        return part['position']

    def setTPAxisAndMarker(self, axis, markers):
        self.trackPoints.setAxis(axis)
        self.trackPoints.setMarkers(markers)
        if not self.carInitialized:
            self.car.setPosition(0)
            self.carInitialized = True



    def setTPParams(self, _camera, _dist):
        self.trackPoints.setParams(_camera, _dist)

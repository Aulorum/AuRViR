import cv2
import numpy as np

class TrackPoints():

    def __init__(self):
        self._dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
        self._board = cv2.aruco.CharucoBoard_create(7, 7, 30, 20, self._dict)
        self.track = []
        self.axis = []
        self._camera = []
        self._dist = []

    def setParams(self, axis, _camera, _dist):
        self.axis = axis
        self._camera = _camera
        self._dist = _dist


    def setMarkers(self, markers):
        ms = markers.getAllMarkers()
        for i in range(len(ms)):
            _, _, rvec, tvec = ms[i]
            points, _ = cv2.projectPoints(self.axis, rvec, tvec, self._camera, self._dist)
            self.track.append(np.mean(points, axis=0))


    def getTrack(self):
        return self.track

    def generateTrackPoints(self, distance):
        pass
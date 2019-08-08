import cv2

class TrackPoints():

    def __init__(self):
        self._dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
        self._board = cv2.aruco.CharucoBoard_create(7, 7, 30, 20, self._dict)
        self.markers = []

    def setMarkers(self, markers):
        self.markers = markers

    def getMarkers(self):
        return self.markers

    def generateTrackPoints(self, distance):
        pass
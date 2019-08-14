import cv2
import numpy as np

class Markers():

    def __init__(self):
        self._dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
        self._board = cv2.aruco.CharucoBoard_create(7, 7, 30, 20, self._dict)
        self.markers = []

    def addMarker(self, marker):
        self.markers.append(marker)

    def addMarker(self, marker, position):
        try:
            self.markers[position] = marker
        except:
            print('Marker could not be set at this position. Use addMarker')

    def getMarker(self, position):
        try:
            return self.markers[position]
        except:
            print('Invalid get Marker with position ' + str(position))
            return None

    def setAllMarkersWithVecs(self, rvecs, tvecs):
        self.markers.clear()
        try:
            for i in range(rvecs.shape[0]):
                transformation = np.zeros((4, 4))
                rotation, _ = cv2.Rodrigues(rvecs[i])
                transformation[0:-1, 0:-1] = rotation
                transformation[0:-1, 3] = tvecs[i]
                transformation[3, 3] = 1.0
                self.markers.append((i, transformation, rvecs[i], tvecs[i]))
        except:
            pass

    def getAllMarkers(self):
        return self.markers
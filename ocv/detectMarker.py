import cv2
from ocv.calibrateCamera import Calibrater

class Detector():

    def __init__(self, _camera, _dist):
        self._dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
        self._board = cv2.aruco.CharucoBoard_create(7, 7, 30, 20, self._dict)
        self._camera = _camera
        self._dist = _dist
        self.img = []
        self.gray = []
        self.markerCorners = []
        self.markerIds = []
        self.markersRejected = []
        self.numberCorners = []
        self.charucoCorners = []
        self.charucoIds = []
        self.imsize = []
        print('Detector initialization finished')

    def loadImage(self, imgNumber):
        try:
            self.img = cv2.imread('Data/Images/test' + str(imgNumber) + '.jpg')
            self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            self.imsize = self.gray.shape
        except:
            print('No Image found')

    def showImage(self):
        cv2.imshow('image', self.img)
        cv2.waitKey(0)

    def detectMarker(self):
        self.markerCorners, self.markerIds, self.markersRejected = \
            cv2.aruco.detectMarkers(self.gray, self._dict)
        cv2.aruco.drawDetectedMarkers(self.img, self.markerCorners, self.markerIds)

    def detectCharucoCorners(self):
        _, self.charucoCorners, self.charucoIds = \
            cv2.aruco.interpolateCornersCharuco(self.markerCorners, self.markerIds, self.gray, self._board)


    def estimatePoses(self):
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(self.markerCorners, 2, self._camera, self._dist)
        for i in range(rvecs.shape[0]):
            cv2.aruco.drawAxis(self.img, self._camera, self._dist, rvecs[i], tvecs[i], 2)

    def getImage(self):
        return self.img

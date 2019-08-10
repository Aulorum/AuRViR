import cv2
import operator
import numpy as np


class Detector:

    def __init__(self, _camera, _dist, useWebcam=True):
        self._dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
        self._board = cv2.aruco.CharucoBoard_create(7, 7, 30, 20, self._dict)
        self._camera = []
        self._dist = []
        self.img = []
        self.gray = []
        self.markerCorners = []
        self.markerIds = []
        self.markersRejected = []
        self.numberCorners = []
        self.charucoCorners = []
        self.charucoIds = []
        self.imsize = []
        self._camera = _camera
        self._dist = _dist
        self.useWebcame = useWebcam
        print('Detector initialization finished')

    def loadImage(self, number):
        self.img = []
        if self.useWebcame:
            cap = cv2.VideoCapture(0)
            ret, img = cap.read()
            self.img = img
            self.imsize = (self.img.shape[0], self.img.shape[1])
            cap.release()

        else:
            try:
                self.img = cv2.imread('Data/Images/new/test' + str(number) + '.jpg')
                self.imsize = self.gray.shape
            except:
                print('No Image found')

    def showImage(self, image):
        cv2.imshow('image', image)
        cv2.waitKey(1)

    def detectMarker(self):
        self.markerCorners, self.markerIds, self.markersRejected = \
            cv2.aruco.detectMarkers(self.img, self._dict)
        # cv2.aruco.drawDetectedMarkers(self.img, self.markerCorners, self.markerIds)
        self.sortMarkers()

    def detectCharucoCorners(self):
        _, self.charucoCorners, self.charucoIds = \
            cv2.aruco.interpolateCornersCharuco(self.markerCorners, self.markerIds, self.img, self._board)

    def estimatePoses(self):
        rvecs, tvecs, axis = cv2.aruco.estimatePoseSingleMarkers(self.markerCorners, 20., self._camera, self._dist)
        for i in range(rvecs.shape[0]):
            cv2.aruco.drawAxis(self.img, self._camera, self._dist, rvecs[i], tvecs[i], 10)

        return rvecs, tvecs, axis

    def sortMarkers(self):
        combinedMarkers = list(zip(self.markerIds.tolist(), self.markerCorners))
        combinedMarkers.sort(key=operator.itemgetter(0))
        self.markerIds, self.markerCorners = list(zip(*combinedMarkers))
        self.markerIds = np.asarray(self.markerIds)

    def getImage(self):
        return self.img


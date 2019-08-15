import cv2
import operator
import numpy as np
import time

class Detector:

    def __init__(self, _camera, _dist, useWebcam=True):
        self._dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
        self._board = cv2.aruco.CharucoBoard_create(7, 7, 30, 20, self._dict)
        self._camera = []
        self._dist = []
        self.img = []
        self.gray = []
        self.markerCorners = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.markerIds = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        self.markersRejected = []
        self.numberCorners = []
        self.charucoCorners = []
        self.charucoIds = []
        self.imsize = []
        self.gray = []
        self._camera = _camera
        self._dist = _dist
        self.useWebcame = useWebcam
        # Use (1) at notebook
        self.cap = cv2.VideoCapture(0)
        self.possible_ids = []
        self.start_time = 0


    def startTimer(self):
        self.start_time = time.time()

    def loadImage(self, number):
        self.img = []
        if self.useWebcame:
            ret, img = self.cap.read()
            self.img = img
            self.gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            self.imsize = (self.img.shape[0], self.img.shape[1])
        else:
            try:
                self.img = cv2.imread('Data/Images/new/test' + str(number) + '.jpg')
                self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
                self.imsize = self.gray.shape
            except:
                print('No Image found')

    def showImage(self, image):
        cv2.imshow('image', image)
        cv2.waitKey(1)

    def detectMarker(self):
        markerCorners, markerIds, self.markersRejected = \
            cv2.aruco.detectMarkers(self.gray, self._dict)
        self.sortMarkers(markerCorners, markerIds)
        if self.possible_ids.__len__() == self.markerIds.size:
            return True
        else:
            if time.time()-self.start_time > 5:
                self.renewallallowedmarkers()
                print(time.time()-self.start_time)
            return False

    def drawMarker(self):
        cv2.aruco.drawDetectedMarkers(self.img, self.markerCorners, self.markerIds)

    def detectCharucoCorners(self):
        if not self.markerCorners.__len__() == 0:
            _, self.charucoCorners, self.charucoIds = \
                cv2.aruco.interpolateCornersCharuco(self.markerCorners, self.markerIds, self.img, self._board)
        else:
            print('No markers found')

    def estimatePoses(self):
        rvecs = []
        tvecs = []
        axis = []
        if not self.markerCorners.__len__() == 0:
            rvecs, tvecs, axis = cv2.aruco.estimatePoseSingleMarkers(self.markerCorners, 20., self._camera, self._dist)
            #for i in range(rvecs.shape[0]):
                #cv2.aruco.drawDetectedMarkers(self.img, self.markerCorners, self.markerIds) #, self._camera, self._dist, rvecs[i], tvecs[i], 10)

        return rvecs, tvecs, axis

    def sortMarkers(self, markers, ids):
        if not markers.__len__() == 0:
            for i in range(markers.__len__()):
                index = np.where(self.markerIds == ids[i])[0]
                if not len(index) == 0:
                    try:
                        self.possible_ids.index(ids[i][0])
                    except:
                        self.possible_ids.append(ids[i][0])
                    self.markerCorners[index[0]] = markers[i]

            combinedMarkers = list(zip(self.markerIds.tolist(), self.markerCorners))
            combinedMarkers.sort(key=operator.itemgetter(0))
            self.markerIds, self.markerCorners = list(zip(*combinedMarkers))
            self.markerCorners = list(self.markerCorners)
            self.markerIds = np.asarray(self.markerIds)

    def getImage(self):
        return self.img

    def renewallallowedmarkers(self):
        self.possible_ids.sort()
        mids = self.markerIds.tolist()
        h = []
        for i in mids:
            try:
                self.possible_ids.index(i)
                h.append(self.markerCorners[i-1])
            except:
                index = np.argwhere(self.markerIds==i)
                self.markerIds = np.delete(self.markerIds, index)
        self.markerCorners = h
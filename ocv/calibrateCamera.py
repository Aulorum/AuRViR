import cv2

class Calibrater():

    def __init__(self):
        self._dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
        self._board = cv2.aruco.CharucoBoard_create(7, 7, 30, 20, self._dict)
        self._camera = []
        self._dist = []

    def calibrate(self):
        allCorners = []
        allIds = []
        for i in range(12):
            img = cv2.imread('Data/Images/new/test' + str(i) + '.jpg')
            imsize = (img.shape[0], img.shape[1])

            res = cv2.aruco.detectMarkers(img, self._dict)
            if len(res[0]) > 0:
                res2 = cv2.aruco.interpolateCornersCharuco(res[0], res[1], img, self._board)
                allCorners.append(res2[1])
                allIds.append(res2[2])

            cv2.aruco.drawDetectedMarkers(img, res[0], res[1])
            cv2.imshow('frame', img)
            cv2.waitKey(2)

            try:
                err, self._camera, self._dist, _, _ = cv2.aruco.calibrateCameraCharuco(allCorners, allIds, self._board,
                                                                                       imsize, None, None)
            except:
                print('Calibration some err')

            print('Calibation Error ' + str(err) + " in Iteration " + str(i))

            if err < 2.0 and i > 3:
                break

        cv2.destroyAllWindows()

    def getParameters(self):
        return self._camera, self._dist
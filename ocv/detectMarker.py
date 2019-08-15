import cv2
import operator
import numpy as np
import time
import math
from ocv.objectLoader import OBJ

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
        self.cap = cv2.VideoCapture(1)
        self.possible_ids = []
        self.start_time = 0
        self.marker_models = []
        for i in range(12):
            self.marker_models.append(cv2.imread("Data/Marker/marker" + str(i) + ".png"))
        self.orb = cv2.ORB_create()
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        self.min_matches = 8


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
            if time.time()-self.start_time > 3:
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

    def estimateHomography(self, marker, obj):
        model = self.marker_models[marker-1]
        kp_model, des_model = self.orb.detectAndCompute(model, None)
        kp_frame, des_frame = self.orb.detectAndCompute(self.img, None)
        matches = self.bf.match(des_model, des_frame)
        matches = sorted(matches, key=lambda x: x.distance)
        if len(matches) > self.min_matches:
            src_pts = np.float32([kp_model[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp_frame[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
            # Compute Homography
            homography, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            if homography is not None:
                projection = self.projection_matrix(self._camera, homography)
                # project cube or model
                self.img = self.render(self.img, obj, projection, model, False)
                try:
                    # obtain 3D projection matrix from homography matrix and camera parameters
                    pass
                    # frame = render(frame, model, projection)
                except:
                    print('Homography bug')
                    pass
            else:
                print('Homogpraphy.none')

        else:
            print('not enough matches')
        pass

    def projection_matrix(self, camera_parameters, homography):
        """
        From the camera calibration matrix and the estimated homography
        compute the 3D projection matrix
        """
        # Compute rotation along the x and y axis as well as the translation
        homography = homography * (-1)
        rot_and_transl = np.dot(np.linalg.inv(camera_parameters), homography)
        col_1 = rot_and_transl[:, 0]
        col_2 = rot_and_transl[:, 1]
        col_3 = rot_and_transl[:, 2]
        # normalise vectors
        l = math.sqrt(np.linalg.norm(col_1, 2) * np.linalg.norm(col_2, 2))
        rot_1 = col_1 / l
        rot_2 = col_2 / l
        translation = col_3 / l
        # compute the orthonormal basis
        c = rot_1 + rot_2
        p = np.cross(rot_1, rot_2)
        d = np.cross(c, p)
        rot_1 = np.dot(c / np.linalg.norm(c, 2) + d / np.linalg.norm(d, 2), 1 / math.sqrt(2))
        rot_2 = np.dot(c / np.linalg.norm(c, 2) - d / np.linalg.norm(d, 2), 1 / math.sqrt(2))
        rot_3 = np.cross(rot_1, rot_2)
        # finally, compute the 3D projection matrix from the model to the current frame
        projection = np.stack((rot_1, rot_2, rot_3, translation)).T
        return np.dot(camera_parameters, projection)

    def render(self, img, obj, projection, model, color=False):
        """
        Render a loaded obj model into the current video frame
        """
        vertices = obj.vertices
        scale_matrix = np.eye(3) * 3
        h, w = model.shape[0:2]

        for face in obj.faces:
            face_vertices = face[0]
            points = np.array([vertices[vertex - 1] for vertex in face_vertices])
            points = np.dot(points, scale_matrix)
            # render model in the middle of the reference surface. To do so,
            # model points must be displaced
            points = np.array([[p[0] + w / 2, p[1] + h / 2, p[2]] for p in points])
            dst = cv2.perspectiveTransform(points.reshape(-1, 1, 3), projection)
            imgpts = np.int32(dst)
            if color is False:
                cv2.fillConvexPoly(img, imgpts, (137, 27, 211))
            else:
                color = self.hex_to_rgb(face[-1])
                color = color[::-1]  # reverse
                cv2.fillConvexPoly(img, imgpts, color)

        return img

    def hex_to_rgb(self, hex_color):
        """
        Helper function to convert hex strings to RGB
        """
        hex_color = hex_color.lstrip('#')
        h_len = len(hex_color)
        return tuple(int(hex_color[i:i + h_len // 3], 16) for i in range(0, h_len, h_len // 3))
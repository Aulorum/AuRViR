import cv2
import numpy as np
import time

class TrackPoints():

    def __init__(self, _camera, _dist):
        self._dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
        self._board = cv2.aruco.CharucoBoard_create(7, 7, 30, 20, self._dict)
        self.track = []
        self.markers = []
        self.axis = []
        self._camera = _camera
        self._dist = _dist

    def setAxis(self, axis):
        self.axis = []
        self.axis = axis

    def setMarkers(self, markers):
        self.markers.clear()
        ms = markers.getAllMarkers()
        for i in range(ms.__len__()):
            try:
                _, _, rvec, tvec = ms[i]
                points, _ = cv2.projectPoints(self.axis, rvec, tvec, self._camera, self._dist)
                # Set trackpoints with id, position (and maybe position for panda3d)
                self.markers.append({'id': i, 'position': np.mean(points, axis=0, dtype=int)[0], 'position3D': [rvec[0], tvec[0]]})
            except:
                break
        self.generateTrackPoints(100)


    def getTrack(self):
        return self.track

    def getPart(self, num):
        return self.track[num]

    def getPartForCar(self, num):
        try:
            return self.track[num], num
        except:
            pass

    def getVector(self, marker):
        if marker == len(self.track)-1:
            part1 = self.track[marker]['position']
            part2 = self.track[0]['position']
        else:
            part1 = self.track[marker]['position']
            part2 = self.track[marker+1]['position']
        vec = part2-part1
        return vec/np.sum(vec)

    def getVector3D(self, pos):
        if pos < len(self.track)-1:
            part1 = self.track[pos]['position3D']
            part2 = self.track[pos+1]['position3D']
        else:
            part1 = self.track[pos]['position3D']
            part2 = self.track[0]['position3D']
        vec = part2 - part1
        return vec

    def generateTrackPoints(self, distance):
        partNum = 0
        self.track.clear()
        try:
            for i in range(self.markers.__len__()):
                m1 = self.markers[i]
                if i == m1['id']:
                    if i < self.markers.__len__()-1:
                        m2 = self.markers[i+1]
                        h = np.linspace(m1['position'], m2['position'], distance)
                        h3d = np.linspace(m1['position3D'][1], m2['position3D'][1], distance)
                    else:
                        m2 = self.markers[0]
                        h = np.linspace(m1['position'], m2['position'], distance)
                        h3d = np.linspace(m1['position3D'][1], m2['position3D'][1], distance)
                    for j in range(distance):
                        self.track.append({'id': partNum, 'position': h[j].astype(int), 'position3D': h3d[j]})
                        partNum += 1
                else:
                    break
        except:
            pass

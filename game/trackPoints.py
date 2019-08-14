import cv2
import numpy as np

class TrackPoints():

    def __init__(self, _camera, _dist, maxMarkerId):
        self._dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
        self._board = cv2.aruco.CharucoBoard_create(7, 7, 30, 20, self._dict)
        self.track = []
        self.markers = []
        self.axis = []
        self._camera = _camera
        self._dist = _dist
        self.maxMarkerId = maxMarkerId

    def setAxis(self, axis):
        self.axis = []
        self.axis = axis

    def setMarkers(self, markers):
        self.markers.clear()
        ms = markers.getAllMarkers()
        for i in range(self.maxMarkerId):
            try:
                _, _, rvec, tvec = ms[i]
                points, _ = cv2.projectPoints(self.axis, rvec, tvec, self._camera, self._dist)
                # Set trackpoints with id, position (and maybe position for panda3d)
                self.markers.append({'id': i, 'position': np.mean(points, axis=0, dtype=int)[0]})
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

    def generateTrackPoints(self, distance):
        self.track.clear()
        partNum = 0
        try:
            for i in range(self.maxMarkerId):
                m1 = self.markers[i]
                if i == m1['id']:
                    if i < self.maxMarkerId-1:
                        m2 = self.markers[i+1]['position']
                        h = np.linspace(m1['position'], m2, distance)

                    else:
                        m2 = self.markers[0]['position']
                        h = np.linspace(m1['position'], m2, distance)
                    for j in range(distance):
                        self.track.append({'id': partNum, 'position': h[j].astype(int)})
                        partNum += 1
                else:
                    break
        except:
            pass
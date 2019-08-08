import cv2
import numpy as np

class OpenCVDrawer():

    def __init__(self):
        self.trackPoints = []
        self.image = []

    def setTrackPoints(self, trackPoints):
        self.trackPoints = trackPoints

    def setImage(self, image):
        self.image = image

    def getImage(self):
        return self.image

    def drawLine(self, start, finish):
        offset = np.asarray(((int)(self.image.shape[0]/2), (int)(self.image.shape[1]/2)))
        h = tuple(start)
        self.image = cv2.line(self.image, tuple(start+offset), tuple(finish+offset), (0, 255, 0), 5)
        pass

    def drawTrack(self, number_of_markers):
        for i in range(number_of_markers):
            if i == number_of_markers-1:
                pass
            else:
                markers = self.trackPoints.getMarkers()
                h1 = (markers.getMarker(i)[1][0:-2, 3]*10).astype(int)
                h2 = (markers.getMarker(i+1)[1][0:-2, 3]*10).astype(int)
                self.drawLine(h1, h2)
                pass
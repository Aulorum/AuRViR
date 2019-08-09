import cv2
from ocv.detectMarker import Detector
from ocv.calibrateCamera import Calibrater
from ocv.markers import Markers
from ocv.trackPoints import TrackPoints
from ocv.opencvDrawer import OpenCVDrawer
from matplotlib import pyplot as plt
from p3d.renderer import Renderer
# from pogl.renderer import Renderer

if __name__ == '__main__':
    # Initialize stuff
    calibrater = Calibrater()
    markers = Markers()
    trackPoints = TrackPoints()
    detector = Detector()
    opencvDrawer = OpenCVDrawer()
    # Calibrate to get _camera and distortion
    calibrater.calibrate()
    _camera, _dist = calibrater.getParameters()
    detector.setParams(_camera, _dist)

    while True:
        # Detector and with _camera and _dist initialized
        detector.loadImage(0)
        detector.detectMarker()
        detector.detectCharucoCorners()
        rvecs, tvecs, axis = detector.estimatePoses()
        image = detector.getImage()
        markers.setAllMarkersWithVecs(rvecs, tvecs)
        trackPoints.setParams(axis, _camera, _dist)
        trackPoints.setMarkers(markers)
        opencvDrawer.setParams(axis, _camera, _dist)
        opencvDrawer.setTrackPoints(trackPoints)
        opencvDrawer.setImage(image)
        opencvDrawer.drawTrack(5)
        opencvDrawer.drawCar()
        #opencvDrawer.drawLine((0, 0), (300, 300), color=(0, 0, 255))
        #opencvDrawer.drawLine((-120, -210), (300, 300), color=(0, 0, 255))
        image = opencvDrawer.getImage()
        cv2.imshow('image', image)
        cv2.waitKey(1)
        print('Hi')


    #
    # renderer = Renderer(image)
    # renderer.showImage(image)
    print('End')
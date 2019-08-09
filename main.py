import cv2
from ocv.detectMarker import Detector
from ocv.calibrateCamera import Calibrater
from ocv.markers import Markers
from ocv.opencvDrawer import OpenCVDrawer
from game.game import Game
# from pogl.renderer import Renderer

if __name__ == '__main__':
    markersUsed = 5

    # Initialize stuff
    calibrater = Calibrater()
    markers = Markers()
    # Calibrate to get _camera and distortion
    calibrater.calibrate()
    _camera, _dist = calibrater.getParameters()

    detector = Detector(_camera, _dist)
    game = Game(_camera, _dist, markersUsed)
    opencvDrawer = OpenCVDrawer(_camera, _dist)

    # To set car base Position
    detector.loadImage(0)
    detector.detectMarker()
    detector.detectCharucoCorners()
    rvecs, tvecs, axis = detector.estimatePoses()
    markers.setAllMarkersWithVecs(rvecs, tvecs)
    game.setTPAxisAndMarker(axis, markers)

    while True:
        image = []
        game.step()
        detector.loadImage(1)
        detector.detectMarker()
        detector.detectCharucoCorners()
        rvecs, tvecs, axis = detector.estimatePoses()
        image = detector.getImage()
        markers.setAllMarkersWithVecs(rvecs, tvecs)
        game.setTPAxisAndMarker(axis, markers)
        opencvDrawer.setAxisImage(axis, image)
        opencvDrawer.setTrackPoints(game.getTrackPoints())
        opencvDrawer.drawTrack(markersUsed)
        opencvDrawer.drawCar(game.getCarPosition())
        image = opencvDrawer.getImage()
        cv2.imshow('image', image)
        cv2.waitKey(1)

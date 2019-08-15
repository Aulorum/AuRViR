import cv2
import time
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
    game = Game(_camera, _dist)
    opencvDrawer = OpenCVDrawer(_camera, _dist, detector)

    time.sleep(5)

    # To set car base Position
    detector.loadImage(0)
    detector.startTimer()
    all_detected = detector.detectMarker()
    # detects Charuco Corners
    # Estimates marker poses
    if all_detected:
        rvecs, tvecs, axis = detector.estimatePoses()
        markers.setAllMarkersWithVecs(rvecs, tvecs)
        game.setTPAxisAndMarker(axis, markers)

    while True:

        start = time.time()
        image = []
        # Loads Image from Webcam
        detector.loadImage(1)
        # Detects Marker
        all_detected = detector.detectMarker()
        # detects Charuco Corners
        # Estimates marker poses
        if all_detected:
            rvecs, tvecs, axis = detector.estimatePoses()
            # Gets Image
            image = detector.getImage()
            # sets Markers
            markers.setAllMarkersWithVecs(rvecs, tvecs)
            # Set Axis, markers
            game.setTPAxisAndMarker(axis, markers)
            game.step()
            # Sets image in opencvDrawer
            opencvDrawer.setAxisImage(axis, image)
            opencvDrawer.setTrackPoints(game.getTrackPoints())
            opencvDrawer.drawTrack()
            opencvDrawer.drawCar(game.getCarPosition())
            image = opencvDrawer.getImage()
            print(time.time()-start)
            cv2.imshow('image', image)
            cv2.waitKey(1)
        else:
            #detector.drawMarker()
            image = detector.getImage()
            cv2.imshow('image', image)
            cv2.waitKey(1)



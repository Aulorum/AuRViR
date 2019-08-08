from ocv.detectMarker import Detector
from ocv.calibrateCamera import Calibrater
# from p3d.renderer import Renderer
from pogl.renderer import Renderer

if __name__ == '__main__':
    calibrater = Calibrater()
    calibrater.calibrate()
    _camera, _dist = calibrater.getParameters()
    detector = Detector(_camera, _dist)
    detector.loadImage(0)
    detector.detectMarker()
    detector.detectCharucoCorners()
    detector.estimatePoses()
    image = detector.getImage()
    detector.showImage()
    renderer = Renderer()
    renderer.showImage(image)
    print('End')
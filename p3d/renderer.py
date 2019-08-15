from direct.gui.DirectFrame import DirectFrame
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from math import pi, sin, cos
from direct.task import Task
import numpy
from direct.showbase.DirectObject import DirectObject

#needs image, carPos, trackDir


class Renderer(ShowBase):
    def __init__(self, image, carPos, trackDir):
        ShowBase.__init__(self)
        self.image = image
        # add show image function
        #OnscreenImage(image=image, pos=(0, 0, 0))
        bg = DirectFrame(image=image, sortOrder=(-1))
        bg.setPos(0, 20, 0)
        bg.reparentTo(render2d)

        nrDisplayRegions = self.camera.getNumDisplayRegions()
        print(nrDisplayRegions)
        self.carPos = carPos
        self.carModel = None
        self.loadModels(carPos)
        self.trackDir = trackDir
        # EXAMPLE CODE
        # Add the spinCameraTask procedure to the task manager.
        #self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    def loadModels(self, carPos):
        self.carModel = loader.loadModel("../Data/Models/Car.egg")
        self.carModel.reparentTo(render)
        self.carModel.setScale(1, 1, 1)
        self.carModel.setPos(carPos[0], carPos[1], carPos[2])
        self.carModel.setH(self.carModel, 180)

    def update(self, image, carPos, trackDir):
        self.carModel.setPos(carPos[0], carPos[1], carPos[2])

        #set rotation of car using trackDir

# EXAMPLE CODE
# Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 0)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont


game = Renderer("../Data/Images/hubble_crabnebula.jpg", numpy.array([0, 10, 0]), 1)
game.run()
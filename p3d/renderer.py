from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from math import pi, sin, cos
from direct.task import Task

#needs image, carPos, trackDir
class Renderer(ShowBase):
    def __init__(self, image, carPos, trackDir):
        ShowBase.__init__(self)
        self.image = image
        # add show image function
        self.carPos = carPos
        self.carModel = None
        self.loadModels()
        self.trackDir = trackDir
        # EXAMPLE CODE
        # Add the spinCameraTask procedure to the task manager.
        #self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    def loadModels(self):
        self.carModel = loader.loadModel("../Data/Models/Car.egg")
        self.carModel.reparentTo(render)
        self.carModel.setScale(1, 1, 1)
        self.carModel.setPos(0, 10, 0)

    def update(self, image, carPos, trackDir):
        # add show image function

        # use carPos
        #self.carModel.setPos(x, y, z)

        #set rotation of car using trackDir

# EXAMPLE CODE
# Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 0)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

game = Renderer(image, carPos, trackDir)
game.run()
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage

class Renderer(ShowBase):
    def __init__(self, image):
        ShowBase.__init__(self)
        imageObject = OnscreenImage(image=image)

    def showImage(self, image):
        imageObject = OnscreenImage(image=image)
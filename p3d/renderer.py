from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage

class Renderer(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

    def setImage(self, image):
        imageObject = OnscreenImage(image=image)
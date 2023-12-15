import adsk.core, adsk.fusion, adsk.cam, traceback, math
from .MachineComponent import *
from .MachineClasses import *

params = MachineParameters()

class MainBase(MachineComponent):

    radius: float
    featureWidth =  0.875

    def __init__(self, transform=None) -> None:
        super().__init__(transform)
        
        self.radius = params.drumRadius.value - 2.8


    ### Sketches!
    def createBearingSketch(self):
        bearingSketch = self.createSketch(self.component.xZConstructionPlane, "Base Pofile")
        
        topRight = Point3D.create(self.radius - self.featureWidth, -0.8, 0)
        leftMiddle = Point3D.create(self.radius, -0.4, 0)
        rightMiddle = Point3D.create(self.radius - self.featureWidth, -0.4, 0)
        bearingSketch.createDimensionedRectangle(topRight, f'{self.featureWidth} cm', '8mm', ReferencePointType.Corner)
        # bearingSketch.createDimensionedCircle(leftMiddle, '2.25 mm')
        bearingSketch.createDimensionedCircle(rightMiddle, '2.25 mm')
        return bearingSketch
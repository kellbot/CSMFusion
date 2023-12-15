import adsk.core, adsk.fusion, adsk.cam, traceback, math
from .MachineComponent import *
from .MachineClasses import *

params = MachineParameters()

# Right now there is no API access to emboss, so these parts must be finished up in the UI. The profiles to emboss are created for them.
class NeedleCam(MachineComponent):
    featureWidth = 1.8 - .1125
    camRadius: float


    def __init__(self) -> None:
        super().__init__()
        self.component.name = "Needle Cam Up"
        # outer radius is the same size as the shell
        self.camRadius = params.shellRadius.value

        self.createBase()
        wallBody = self.createWall()
        self.createScrewHoles(wallBody)
    

    ### Bodies!
    def createBase(self):
        try:
            baseSketch = self.createBaseSketch()
            revolves = self.component.features.revolveFeatures

            midPoint = Point3D.create(params.drumRadius.value + self.featureWidth/2, 0, 0)
            profile = baseSketch.findProfileContainingPoint(midPoint)
            if profile is None:
                raise ValueError(f'Failed to find profile at point ({midPoint.x}, {midPoint.y}, {midPoint.z}')
		
            revolveInput = revolves.createInput(profile, zAxis,FeatureOperations.NewBodyFeatureOperation)
            angle = ValueInput.createByReal(2 * math.pi)
            revolveInput.setAngleExtent(False, angle)
            revolves.add(revolveInput)
        except ValueError as e:
            if ui:
                ui.messageBox(str(e))
        except Exception as e:
            app.log(e)

    def createWall(self):
        revolves = self.component.features.revolveFeatures
        wallSketch = self.createWallSketch()
        profile = wallSketch.sketch.profiles.item(0)

        revolveInput = revolves.createInput(profile, zAxis, FeatureOperations.JoinFeatureOperation)
        angle = ValueInput.createByReal(2 * math.pi)
        revolveInput.setAngleExtent(False, angle)
        wall = revolves.add(revolveInput)
        wallBody = wall.bodies.item(0)

       
        self.createCamSketch()
        return wallBody

    ### Sketches!
    def createBaseSketch(self):
        # This sketch is viewed from the back
        # FUN FACT: When creating a sketch Fusion decides on the coordinate system and you can't change it. This time, up is down and left is right!
        baseSketch = self.createSketch(self.component.xZConstructionPlane, "Base Pofile")
        
        topRight = Point3D.create(self.camRadius - self.featureWidth, -0.8, 0)
        leftMiddle = Point3D.create(self.camRadius, -0.4, 0)
        rightMiddle = Point3D.create(self.camRadius - self.featureWidth, -0.4, 0)
        baseSketch.createDimensionedRectangle(topRight, f'{self.featureWidth} cm', '8mm', ReferencePointType.Corner)
        baseSketch.createDimensionedCircle(leftMiddle, '2.25 mm')
        baseSketch.createDimensionedCircle(rightMiddle, '2.25 mm')
        return baseSketch
    
    # This sketch is viewed from the back
    def createWallSketch(self) -> adsk.fusion.Sketch:
        wallSketch = self.createSketch(self.component.xZConstructionPlane, "Wall Profile")
        topRight = Point3D.create(self.camRadius - 1.25, -4.5, 0)
        lines = wallSketch.createDimensionedRectangle(topRight, '7.75 mm', '45 - 8 mm', ReferencePointType.Corner)
        return wallSketch

    # now we're turned 90 degrees. WHY IS FUSION LIKE THIS
    def createCamSketch(self) -> adsk.fusion.Sketch:
        camSketch = self.createSketch(self.component.yZConstructionPlane, "Cam Up Profile")
        diameterReal = params.drumDiameter.value

        camCircumfrence = math.pi * diameterReal

        ramp = 15 * 120 / diameterReal
        camWidth = ramp / 360 * camCircumfrence

        sketchWidth = diameterReal * 2
        topLeft = Point3D.create(-4.5, 0, 0)
        camSketch.createDimensionedRectangle(topLeft,'45mm',  f'{params.drumDiameter.name} * 2')

        lowerMidline = Point3D.create(0, 0, 0)
        p1 = Point3D.create(  -4.5, camWidth/2, 0)
        line1 = camSketch.sketchLines.addByTwoPoints(lowerMidline, p1)
        p2 = Point3D.create( -3, p1.y + (camWidth/2 * (3/4.5)), 0)
        line2 = camSketch.sketchLines.addByTwoPoints(line1.endSketchPoint, p2)
        camSketch.sketchLines.addByTwoPoints(line2.endSketchPoint, Point3D.create(p2.x, sketchWidth, 0))

    
    def createScrewHoles(self, participantBody):
        features = self.component.features
        # viewed from the back
        sketch = self.machineSketches['Wall Profile']
        center = Point3D.create(0, -2.5, self.camRadius + 1)

        sketch.createDimensionedCircle(center, '1.25 mm')
        profile = sketch.findProfileContainingPoint(center)

        # cut the hole
        extrudeInput = features.extrudeFeatures.createInput(profile, FeatureOperations.CutFeatureOperation)
        extrudeInput.participantBodies = [participantBody]
        extrudeInput.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(ValueInput.createByReal(-3)), adsk.fusion.ExtentDirections.PositiveExtentDirection)


        extrude = features.extrudeFeatures.add(extrudeInput)
        toPattern = adsk.core.ObjectCollection.createWithArray([extrude])

        patternInput = features.circularPatternFeatures.createInput(toPattern, zAxis)
        patternInput.quantity = ValueInput.createByReal(8)
        patternInput.totalAngle = ValueInput.createByReal(2* math.pi)
        patternInput.isSymmetric = False
        features.circularPatternFeatures.add(patternInput)

class DownNeedleCam(MachineComponent):
    def __init__(self) -> None:
        super().__init__()
        self.component.name = "Needle Cam Down"   

import adsk.core, adsk.fusion, adsk.cam, traceback, math
from .utilities import *
from .settings import Settings

app = adsk.core.Application.get()
ui = app.userInterface

product = app.activeProduct
design = adsk.fusion.Design.cast(product)
origin = adsk.core.Point3D.create(0,0,0)
zAxis = design.rootComponent.zConstructionAxis

# More numbers
shellSpacing = 1.3
drumDiameter = Settings.drumDiameter
shellRadius = drumDiameter/2 + shellSpacing
shellThickness = 0.4

def createShell():
    shell = createNewComponent().component
    sketches = shell.sketches
    baseSketch = sketches.add(shell.xYConstructionPlane)

    # extrude the basic shape
    circles = baseSketch.sketchCurves.sketchCircles
    circles.addByCenterRadius(origin, shellRadius)
    circles.addByCenterRadius(origin, shellRadius - shellThickness)

    extrudes = shell.features.extrudeFeatures
    baseInput = extrudes.createInput(baseSketch.profiles.item(0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

    extrudeDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(6.17))

    baseInput.setOneSideExtent(extrudeDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
    baseInput.startExtent = adsk.fusion.OffsetStartDefinition.create(adsk.core.ValueInput.createByReal(0.83))
    baseExtrude = extrudes.add(baseInput)
    topFace = baseExtrude.endFaces.item(0)


    hullSketch = sketches.add(topFace)

   # half moon nub
    circles.addByCenterRadius(adsk.core.Point3D.create(-(shellRadius + 1), 0, 0), 0.4)
    
    domeInput = extrudes.createInput(baseSketch.profiles.item(0), adsk.fusion.FeatureOperations.JoinFeatureOperation)
    extrudeDistance = adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByReal(4.9))

    domeInput.setOneSideExtent(extrudeDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
    domeInput.startExtent = adsk.fusion.OffsetStartDefinition.create(adsk.core.ValueInput.createByReal(2.1))
    extrudes.add(domeInput)

    arcs = hullSketch.sketchCurves.sketchArcs
    arcs.addByCenterStartSweep(adsk.core.Point3D.create(shellRadius + 0.1, -0.6, 0), adsk.core.Point3D.create(shellRadius + 0.1 - 0.5, -0.6, 0), math.pi)
    arcs.addByCenterStartSweep(adsk.core.Point3D.create(shellRadius + 0.1, 0.6, 0), adsk.core.Point3D.create(shellRadius + 0.1 + 0.5, 0.6, 0), math.pi)
    lines = hullSketch.sketchCurves.sketchLines
    lines.addByTwoPoints(adsk.core.Point3D.create(shellRadius + 0.1 - 0.5, -0.6, 0), adsk.core.Point3D.create(shellRadius + 0.1 - 0.5, 0.6, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(shellRadius + 0.1 + 0.5, -0.6, 0), adsk.core.Point3D.create(shellRadius + 0.1 + 0.5, 0.6, 0))
    extrudes.addSimple(hullSketch.profiles.item(1), adsk.core.ValueInput.createByReal(-3.0), adsk.fusion.FeatureOperations.JoinFeatureOperation)


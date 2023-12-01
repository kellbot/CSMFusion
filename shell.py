
import adsk.core, adsk.fusion, adsk.cam, traceback, math
from adsk.core import ValueInput, Point3D
from adsk.fusion import FeatureOperations
from .utilities import *
from .settings import Settings

app = adsk.core.Application.get()
ui = app.userInterface

product = app.activeProduct
design = adsk.fusion.Design.cast(product)
origin = Point3D.create(0,0,0)
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


    hullSketch = sketches.addWithoutEdges(topFace)

   # down cam support
    hullCircles = hullSketch.sketchCurves.sketchCircles
    hullCircles.addByCenterRadius(Point3D.create(-(shellRadius + 0.1), 0, 0), 0.4)
    lines = hullSketch.sketchCurves.sketchLines

    cubeCenter = Point3D.create(-shellRadius, 0, 0)
    lines.addCenterPointRectangle(cubeCenter, Point3D.create(cubeCenter.x + 0.2, cubeCenter.y + 0.4, cubeCenter.z))

    extrudeDistance = ValueInput.createByReal(-4.9)
    extrudes.addSimple(getAllSketchProfiles(hullSketch), extrudeDistance, FeatureOperations.JoinFeatureOperation)



    # create plane tangent to shell at slot point
    planeInput = shell.constructionPlanes.createInput()
    planeInput.setByTangent(baseExtrude.sideFaces.item(1), ValueInput.createByString(str(-90 - (15*(120/drumDiameter)))+'deg'), shell.yZConstructionPlane)
    slotPlane = shell.constructionPlanes.add(planeInput)


    # Creates a slot at a fixed distance from the cam support
    slotSketch = shell.sketches.add(slotPlane)
    slotArcs = slotSketch.sketchCurves.sketchArcs
    slotLines = slotSketch.sketchCurves.sketchLines
    topCenter = Point3D.create(0,3.85, 0)
    bottomCenter = Point3D.create(0,3.85 + 1.1, 0)

    # TODO: Dry this up
    slotArcs.addByCenterStartSweep(topCenter, Point3D.create(-0.8,  topCenter.y, 0), math.pi)
    slotArcs.addByCenterStartSweep(topCenter, Point3D.create(-0.35/2,  topCenter.y, 0), math.pi)

    slotArcs.addByCenterStartSweep(bottomCenter, Point3D.create(-0.8,  bottomCenter.y, 0), -math.pi)
    slotArcs.addByCenterStartSweep(bottomCenter, Point3D.create(-0.35/2,  bottomCenter.y, 0), -math.pi)

    slotLines.addByTwoPoints(Point3D.create(-0.8, topCenter.y, 0), Point3D.create(-0.8, bottomCenter.y, 0))
    slotLines.addByTwoPoints(Point3D.create(-0.35/2, topCenter.y, 0), Point3D.create(-0.35/2, bottomCenter.y, 0))

    slotLines.addByTwoPoints(Point3D.create(0.8, topCenter.y, 0), Point3D.create(0.8, bottomCenter.y, 0))
    
    slotLines.addByTwoPoints(Point3D.create(0.35/2, topCenter.y, 0), Point3D.create(0.35/2, bottomCenter.y, 0))


    slotPadExtrude = extrudes.addSimple(slotSketch.profiles.item(0), ValueInput.createByReal(-0.4),FeatureOperations.JoinFeatureOperation)
    slotExtrude = extrudes.addSimple(slotSketch.profiles.item(1), ValueInput.createByReal(-0.5), FeatureOperations.CutFeatureOperation)


    bumperSketch = createSketchAtAngle(shell.xZConstructionPlane, Settings.camAngle - 9)
    bumperProfileCenter = Point3D.create(1.63, -shellRadius, 0)
    bumperSketch.sketchCurves.sketchCircles.addByCenterRadius(bumperProfileCenter, 0.5)
    revolves = shell.features.revolveFeatures
    revolveInput = revolves.createInput(bumperSketch.profiles.item(0), shell.zConstructionAxis, FeatureOperations.JoinFeatureOperation)
    revolveInput.setAngleExtent(False, ValueInput.createByString('8 deg'))
    bumper1 = revolves.add(revolveInput)
    bumperSketch.sketchCurves.sketchLines.addByTwoPoints(Point3D.create(bumperProfileCenter.x + 0.5, bumperProfileCenter.y, bumperProfileCenter.z ), Point3D.create(bumperProfileCenter.x - 0.5, bumperProfileCenter.y, bumperProfileCenter.z ))
    capProfile = findProfileContainingPoint(bumperSketch, Point3D.create(bumperProfileCenter.x, bumperProfileCenter.y + 0.01, bumperProfileCenter.z))
    capInput = revolves.createInput(capProfile, bumperSketch.sketchCurves.sketchLines.item(0), FeatureOperations.JoinFeatureOperation)
    capInput.setAngleExtent(False, ValueInput.createByString('180 deg'))
    bumper2 = revolves.add(capInput)

    bumper = adsk.core.ObjectCollection.create()
    bumper.add(bumper1)
    bumper.add(bumper2)
    bumper.add(slotPadExtrude)
    bumper.add(slotExtrude)
    mirrors = shell.features.mirrorFeatures
    mirrors.add(mirrors.createInput(bumper, shell.xZConstructionPlane))
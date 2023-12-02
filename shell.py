
import adsk.core, adsk.fusion, adsk.cam, traceback, math
from adsk.core import ValueInput, Point3D
from adsk.fusion import FeatureOperations
from .utilities import *
from .hardware import *
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
    shell.name = "Shell"
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


    outsideFace = baseExtrude.sideFaces.item(1)

    ## Some construction planes for later
  
    # create plane tangent to shell at slot point
    planeInput = shell.constructionPlanes.createInput()
    planeInput.setByTangent(outsideFace, ValueInput.createByString(str(-90 - (15*(120/drumDiameter)))+'deg'), shell.yZConstructionPlane)
    slotPlane = shell.constructionPlanes.add(planeInput)
    slotPlane.name = "Front Tangent Plane"

    # create plane tangent to shell at back
    planeInput = shell.constructionPlanes.createInput()
    planeInput.setByTangent(outsideFace, ValueInput.createByString(str(0)+'deg'), shell.yZConstructionPlane)
    backPlane = shell.constructionPlanes.add(planeInput)

    # create a plane 45 degrees off the cam support
    planeInput = shell.constructionPlanes.createInput()
    planeInput.setByTangent(outsideFace, ValueInput.createByString(str(90 + 45)+'deg'), shell.yZConstructionPlane)
    outsidePlane45 = shell.constructionPlanes.add(planeInput)


    topFace = baseExtrude.endFaces.item(0)



    hullSketch = sketches.addWithoutEdges(topFace)
    # hull cutout, for later
    cutoutSketch = sketches.addWithoutEdges(topFace)
   # down cam support
    hullCircles = hullSketch.sketchCurves.sketchCircles
    circleCenter = Point3D.create(-(shellRadius + 0.1), 0, 0)
    hullSketch.sketchCurves.sketchArcs.addByCenterStartSweep(circleCenter, Point3D.create(circleCenter.x, circleCenter.y + 0.4, circleCenter.z ), math.pi)
    lines = hullSketch.sketchCurves.sketchLines

    cubeCenter = Point3D.create(-shellRadius, 0, 0)
    lines.addCenterPointRectangle(cubeCenter, Point3D.create(circleCenter.x, cubeCenter.y + 0.4, cubeCenter.z))
    
    #hole in the middle
    hullCircles.addByCenterRadius(circleCenter, 0.15)
 
    camSupportProfiles = getAllSketchProfiles(hullSketch)

    extrudeDistance = ValueInput.createByReal(-4.9)
    camSupportExtrude = extrudes.addSimple(camSupportProfiles, extrudeDistance, FeatureOperations.JoinFeatureOperation)   
    camSupportExtrude.name = "Down Cam Support"
 
    adjusterProfiles = adsk.core.ObjectCollection.create()

    adjusterProfiles.add(findProfileContainingPoint(hullSketch, Point3D.create( circleCenter.x - 0.1, 0, 0)))
    adjusterProfiles.add(findProfileContainingPoint(hullSketch, Point3D.create( circleCenter.x + 0.1, 0, 0)))

    adjusterExtrude = extrudes.addSimple(adjusterProfiles, ValueInput.createByReal(-3),  FeatureOperations.CutFeatureOperation)
    adjusterExtrude.name = "Cam adjuster hole"




    # Creates a slot at a fixed distance from the cam support
    slotSketch = shell.sketches.add(slotPlane)
    slotSketch.name = "Slot Sketch"
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


    bumperSketch = createSketchAtAngle(shell.xZConstructionPlane, Settings.ramp() + 9)
    bumperSketch.name = "Bumper Sketch"
    bumperProfileCenter = Point3D.create(1.63, -shellRadius, 0)
    bumperSketch.sketchCurves.sketchCircles.addByCenterRadius(bumperProfileCenter, 0.5)
    bumperSketch.sketchCurves.sketchLines.addByTwoPoints(Point3D.create(bumperProfileCenter.x + 0.5, bumperProfileCenter.y, bumperProfileCenter.z ), Point3D.create(bumperProfileCenter.x - 0.5, bumperProfileCenter.y, bumperProfileCenter.z ))

    revolves = shell.features.revolveFeatures
    bumperProfile = findProfileContainingPoint(bumperSketch, Point3D.create(bumperProfileCenter.x, bumperProfileCenter.y - 0.01, bumperProfileCenter.z))
    revolveInput = revolves.createInput(bumperProfile, shell.zConstructionAxis, FeatureOperations.JoinFeatureOperation)
    revolveInput.setAngleExtent(False, ValueInput.createByString('8 deg'))
    bumper1 = revolves.add(revolveInput)

    capInput = revolves.createInput(bumperProfile, bumperSketch.sketchCurves.sketchLines.item(0), FeatureOperations.JoinFeatureOperation)
    capInput.setAngleExtent(False, ValueInput.createByString('-100 deg'))
    bumper2 = revolves.add(capInput)

    bumper = adsk.core.ObjectCollection.create()
    bumper.add(bumper1)
    bumper.add(bumper2)
    bumper.add(slotPadExtrude)
    bumper.add(slotExtrude)
    mirrors = shell.features.mirrorFeatures
    mirrors.add(mirrors.createInput(bumper, shell.xZConstructionPlane))

    # down_cam cutout
    cutoutCenter = Point3D.create(-shellRadius, 0, -1.25)
    cutoutSize = {"x": 2, "y": .84, "z": 3.1}
    # I already regret how I set this up
    cornerPoint = createPointByOffset(cutoutCenter, {"x": cutoutSize["x"]/2, "y": cutoutSize["y"]/2, "z": 0})
    cutoutSketch.sketchCurves.sketchLines.addCenterPointRectangle(cutoutCenter, cornerPoint)
    extrudes.addSimple(cutoutSketch.profiles.item(0), ValueInput.createByReal(-cutoutSize["z"]), FeatureOperations.CutFeatureOperation)
    createM3NutCutout(cutoutSketch.referencePlane, Point3D.create( -shellRadius, 0, -1.25))
    # bit at bottom for cam, borrowing circleCenter from above which is probably a mistake
    cutoutSketch.sketchCurves.sketchCircles.addByCenterRadius(Point3D.create(circleCenter.x, circleCenter.y, -1.25 - cutoutSize["z"]), 0.25)
    extrudes.addSimple(cutoutSketch.profiles.item(cutoutSketch.profiles.count - 1), ValueInput.createByReal(-0.25), FeatureOperations.CutFeatureOperation)

    # a hole for a mysterious magnet
    magnetSketch = sketches.add(backPlane)
    magnetSketch.sketchCurves.sketchCircles.addByCenterRadius(Point3D.create(-6, 0, 0), 0.125)
    extrudes.addSimple(magnetSketch.profiles.item(0), ValueInput.createByReal(-1), FeatureOperations.CutFeatureOperation)

    # holes for cams to line up
    alignmentSketch = sketches.add(outsidePlane45)
    alignmentSketch.sketchCurves.sketchCircles.addByCenterRadius(Point3D.create(0, 2.5, 0), 0.35/2)
    holeExtrude = extrudes.addSimple(alignmentSketch.profiles.item(0), ValueInput.createByReal(-shellThickness - 0.5), FeatureOperations.CutFeatureOperation)
    holes = adsk.core.ObjectCollection.create()
    holes.add(holeExtrude)
    circularPattern(holes, 7, -270)
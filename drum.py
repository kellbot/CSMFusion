#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback, math, json
from .utilities import *
from .settings import Settings

app = adsk.core.Application.get()
ui = app.userInterface

product = app.activeProduct
design = adsk.fusion.Design.cast(product)
origin = adsk.core.Point3D.create(0,0,0)
zAxis = design.rootComponent.zConstructionAxis

unitsMgr = design.fusionUnitsManager
unitsMgr.distanceDisplayUnits = adsk.fusion.DistanceUnits.MillimeterDistanceUnits

#everything is in CM, which is terrible but I don't know how to change it
# settings
drumDiameter = Settings.drumDiameter
drumRadius = drumDiameter/2
drumInnerDiameterMain = drumDiameter - 1.1*2
drumFootThickness = 1.5
drumNeedleCount = 134
drumFloorHeight = adsk.core.ValueInput.createByReal(2.0)

# Fixed variables
drumHeight = 9.25

needleSlotDepth = .75
needleSlotWidth = .17
needleSlotTopWidth = .36
needleSlotHeight = adsk.core.ValueInput.createByReal(7.6)
needleSlotTopHeight = 2.0

drumTopChamferHeight = drumHeight - 8

# creates a sketch on the xy plane for the drum bottom
def drawDrumBase(drumComponent: adsk.fusion.Component, gapWidth: float):

 
    sketches = drumComponent.sketches
    sketch = sketches.add(drumComponent.xYConstructionPlane)
    circles = sketch.sketchCurves.sketchCircles
    rectangles = sketch.sketchCurves.sketchLines
    sketchPoints = sketch.sketchPoints
    
    # Create sketch point at origin
    originPoint = sketchPoints.add(origin)

    # outer edge
    circles.addByCenterRadius(origin, drumRadius)
    # inner edge
    circles.addByCenterRadius(origin, drumInnerDiameterMain/2)
    # needle spaces
    pointA = adsk.core.Point3D.create(drumRadius - needleSlotDepth, -gapWidth/2, 0)
    pointB = adsk.core.Point3D.create(drumRadius + 1, gapWidth/2, 0)
    gap = rectangles.addTwoPointRectangle(pointA, pointB)
    lines = []
    for i in range(gap.count):
      lines.append(gap.item(i))

    
    patternInput = sketch.geometricConstraints.createCircularPatternInput(lines, originPoint)
    patternInput.quantity = adsk.core.ValueInput.createByReal(drumNeedleCount)
    sketch.geometricConstraints.addCircularPattern(patternInput)

    return sketch

# Individual parts
def createDrum():
    
    drum = createNewComponent().component
    if not design:
        ui.messageBox('Workspace not supported, change to MODEL workspace and try again')
        return
    

    lowerSketch = drawDrumBase(drum, needleSlotWidth)
    upperSketch = drawDrumBase(drum, needleSlotTopWidth)
    extrudes = drum.features.extrudeFeatures


    drumProfile = findProfileContainingPoint(lowerSketch,  adsk.core.Point3D.create(drumRadius -  needleSlotDepth - .01, 0, 0))
    drumExtrude = extrudes.addSimple(drumProfile, adsk.core.ValueInput.createByReal(drumHeight - needleSlotTopHeight), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    upperProfile = findProfileContainingPoint(upperSketch, adsk.core.Point3D.create(drumRadius -  needleSlotDepth - .01, 0, 0))
    fullDrumExtrude = extrudes.addSimple(upperProfile, adsk.core.ValueInput.createByReal(drumHeight), adsk.fusion.FeatureOperations.JoinFeatureOperation)

    # Give the body a useful name
    drumBody = fullDrumExtrude.bodies.item(0)
    drumBody.name = "Needle Drum"


    chamferExtrusion(fullDrumExtrude, drumRadius - drumInnerDiameterMain/2 - needleSlotDepth, drumTopChamferHeight )
    
    # add a profile for the foot
    lowerSketch.sketchCurves.sketchCircles.addByCenterRadius(origin, drumRadius - drumFootThickness)
    floorProf = findProfileContainingPoint(lowerSketch, adsk.core.Point3D.create(drumRadius - drumFootThickness + 0.1, 0, 0))
    floorExtrude = extrudes.addSimple(floorProf, drumFloorHeight, adsk.fusion.FeatureOperations.JoinFeatureOperation)
    chamferExtrusion(floorExtrude, 0.4, 1)


    sketch2 = drum.sketches.add(drum.xYConstructionPlane)

    bottomPinSketch = drum.sketches.add(drum.xYConstructionPlane)
    circles = bottomPinSketch.sketchCurves.sketchCircles
    pinRadius = 0.4
    pinHoleRadius = 0.125
    centerY = drumDiameter/2 - 1.3
    circles.addByCenterRadius(adsk.core.Point3D.create(0, centerY, 0), pinRadius)
    circles.addByCenterRadius(adsk.core.Point3D.create(0, centerY, 0), pinHoleRadius)
    circles.addByCenterRadius(adsk.core.Point3D.create(0, centerY, 1.2), pinRadius)
    lines = bottomPinSketch.sketchCurves.sketchLines
    axisLine = lines.addByTwoPoints(adsk.core.Point3D.create(0, centerY - pinRadius, 1.2), adsk.core.Point3D.create(0, centerY + pinRadius, 1.2))
    
    pinFeatures = adsk.core.ObjectCollection.create()
    

    # cylinder of pin
    prof = bottomPinSketch.profiles.item(2) 
    
    pinExtrude = extrudes.addSimple(prof, adsk.core.ValueInput.createByReal(1.2), adsk.fusion.FeatureOperations.JoinFeatureOperation)
    
    pinFeatures.add(pinExtrude)
    # ball on top of pin
    revolves = drum.features.revolveFeatures
    revInput = revolves.createInput(bottomPinSketch.profiles.item(0), axisLine, adsk.fusion.FeatureOperations.JoinFeatureOperation)
    angle = adsk.core.ValueInput.createByReal(2 * math.pi)
    revInput.setAngleExtent(False, angle)
    ballRevolve = revolves.add(revInput)

    pinFeatures.add(ballRevolve)

    

    prof = bottomPinSketch.profiles.item(3)
    holeExtrude = extrudes.addSimple(prof, adsk.core.ValueInput.createByReal(1.2), adsk.fusion.FeatureOperations.CutFeatureOperation)
    
    pinFeatures.add(holeExtrude)

    # create a pattern of 6 pins
    circularPattern(pinFeatures, 6)


    # groove around middle
    sideSketch = drum.sketches.add(drum.xZConstructionPlane)
    circles = sideSketch.sketchCurves.sketchCircles

    circles.addByCenterRadius(adsk.core.Point3D.create(drumRadius - 0.4, -6.5, 0), .2)
    rectangles = sideSketch.sketchCurves.sketchLines
    centerPoint = adsk.core.Point3D.create(drumRadius - 0.4 + 0.16, -6.5, 0 )
    cornerPoint = adsk.core.Point3D.create(drumRadius - 0.4 + 0.32, -6.5 - 0.2, 0 )

    rectangles.addCenterPointRectangle(centerPoint, cornerPoint)

    profs = getAllSketchProfiles(sideSketch)
    revolves = drum.features.revolveFeatures
    revInput = revolves.createInput(profs, zAxis, adsk.fusion.FeatureOperations.CutFeatureOperation)
    angle = adsk.core.ValueInput.createByReal(math.pi* 2)
    revInput.setAngleExtent(False, angle)
    revolves.add(revInput)

    # top rim
    circles.addByCenterRadius(adsk.core.Point3D.create(drumDiameter/2 - needleSlotDepth  - 0.05, -drumHeight, 0), .05)
    revInput = revolves.createInput(sideSketch.profiles.item(3), zAxis, adsk.fusion.FeatureOperations.JoinFeatureOperation)
    revInput.setAngleExtent(False, angle)
    revolves.add(revInput)

    return
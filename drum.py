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

drumThickness = 1.1
drumFootThickness = drumThickness + 0.4
drumNeedleCount = 134
drumFloorHeight = adsk.core.ValueInput.createByReal(2.0)

# Fixed variables
drumHeight = 9.25

needleSlotDepth = .75
needleSlotWidth = .17
needleSlotTopWidth = .36
needleSlotHeight = adsk.core.ValueInput.createByReal(7.6)
needleSlotTopHeight = adsk.core.ValueInput.createByReal(2.0)

drumTopChamferHeight = 1.25

# Individual parts
def createDrum():
    
    drum = createNewComponent().component
    if not design:
        ui.messageBox('Workspace not supported, change to MODEL workspace and try again')
        return
    #create new sketch
    sketches = drum.sketches
    sketch = sketches.add(drum.xYConstructionPlane)

    #extrude the main drum body
    circles = sketch.sketchCurves.sketchCircles
    # outer shell
    circles.addByCenterRadius(origin, drumDiameter/2)
    #inner shell at center
    circles.addByCenterRadius(origin, drumDiameter/2 - drumThickness)
    #inner shell at foot
    circles.addByCenterRadius(origin, drumDiameter/2 - drumFootThickness)
    prof = sketch.profiles.item(0)
    extrudes = drum.features.extrudeFeatures
    drumExtrude = extrudes.addSimple(prof, adsk.core.ValueInput.createByReal(drumHeight), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

    # Give the body a useful name
    drumBody = drumExtrude.bodies.item(0)
    drumBody.name = "Needle Drum"


    chamferExtrusion(drumExtrude, drumThickness - needleSlotDepth - .1, drumTopChamferHeight )


    # extrude the floor/foot
    floorProf = sketch.profiles.item(1)
    floorExtrude = extrudes.addSimple(floorProf, drumFloorHeight, adsk.fusion.FeatureOperations.JoinFeatureOperation)
    # chamfer the foot

    chamferExtrusion(floorExtrude, 0.4, 1)

    sketch2 = sketches.add(drum.xYConstructionPlane)

    bottomPinSketch = sketches.add(drum.xYConstructionPlane)
    circles = bottomPinSketch.sketchCurves.sketchCircles
    pinRadius = 0.4
    pinHoleRadius = 0.125
    centerY = drumDiameter/2 - drumThickness - 0.2
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
    sideSketch = sketches.add(drum.xZConstructionPlane)
    circles = sideSketch.sketchCurves.sketchCircles
    # TODO: Extract these to be relative to thickness
    circles.addByCenterRadius(adsk.core.Point3D.create(drumDiameter/2 - 0.45, -5.8, 0), .2)
    rectangles = sideSketch.sketchCurves.sketchLines
    centerPoint = adsk.core.Point3D.create(drumDiameter/2 - 0.25, -5.8, 0 )
    cornerPoint = adsk.core.Point3D.create(drumDiameter/2 - 0.25 - .16, -5.6, 0 )

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

    # create needle slots
    # We do this late because it's slow to calculate
    # the .05 is just so it won't make extra profiles
    rectangles = sketch2.sketchCurves.sketchLines
    point2 = adsk.core.Point3D.create(drumDiameter/2 + .05 , -needleSlotWidth/2, 0)
    point1 = adsk.core.Point3D.create(drumDiameter/2 - needleSlotDepth, needleSlotWidth/2, 0)
  
    rectangles.addTwoPointRectangle(point1, point2)
    
    slotExtrude = extrudes.addSimple(sketch2.profiles.item(0), needleSlotHeight, adsk.fusion.FeatureOperations.CutFeatureOperation)
    
    # notch at top of slot
    point2 = adsk.core.Point3D.create(drumDiameter/2 + .05 , -needleSlotTopWidth/2, 0)
    point1 = adsk.core.Point3D.create(drumDiameter/2 - needleSlotDepth, needleSlotTopWidth/2, 0)

    rectangles2 = sketch2.sketchCurves.sketchLines
    rectangles2.addTwoPointRectangle(point1, point2)
    profs = getAllSketchProfiles(sketch2)

    extrudeInput = extrudes.createInput(profs, adsk.fusion.FeatureOperations.CutFeatureOperation)
    extrudeDistance = adsk.fusion.DistanceExtentDefinition.create(needleSlotTopHeight)
    extrudeInput.setOneSideExtent(extrudeDistance, adsk.fusion.ExtentDirections.PositiveExtentDirection)
    extrudeInput.startExtent = adsk.fusion.OffsetStartDefinition.create(needleSlotHeight)
    slot2Extrude = extrudes.add(extrudeInput)

    patternEntities = adsk.core.ObjectCollection.create()
    patternEntities.add(slotExtrude)
    patternEntities.add(slot2Extrude)
   
    circularPattern(patternEntities, drumNeedleCount)

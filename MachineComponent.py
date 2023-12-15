import adsk.core, adsk.fusion, adsk.cam, traceback
from .utilities import *
from .MachineClasses import MachineSketch
from typing import Dict

origin = Point3D.create(0,0,0)

class MachineComponent():
    component: adsk.fusion.Component

    machineSketches: Dict[str, MachineSketch] = {}

    def __init__(self, transform = None) -> None:
        if not transform:
            transform = adsk.core.Matrix3D.create()
        self.component = design.rootComponent.occurrences.addNewComponent(transform).component

    def createSketch(self, referencePlane: adsk.core.Base, name: str = None):
        newSketch = MachineSketch(self.component, referencePlane, name)
        self.machineSketches[name] = newSketch
        return newSketch
    
class Knob(MachineComponent):
    knobSketch: MachineSketch 

    def __init__(self, totalHeight, knobThicknessExpression, diameterExpression, name = "Knob", isNut = False, matrix = None) -> None:
        super().__init__(matrix)
        self.component.name = name  
        self.totalHeight = unitsMgr.evaluateExpression(totalHeight)
        self.thickness = unitsMgr.evaluateExpression(knobThicknessExpression)
        self.height = self.totalHeight - self.thickness
        self.diameterExpression = diameterExpression
        self.diameter = unitsMgr.evaluateExpression(diameterExpression)
        self.isNut = isNut

        self.createTop()
        self.createStem()
        self.createGrips()

        if self.isNut:
            pass
        else:
            self.createSocket()

    ## Bodies
    def createSocket(self):
        # hole all the way through
        sketchOrigin = self.knobSketch.originSketchPoint
        extrudes = self.component.features.extrudeFeatures
        knobSketch = self.knobSketch

        knobSketch.createDimensionedCircle(sketchOrigin, "3.25mm")
        profile = knobSketch.findInnermostProfile()
        extrudeInput = extrudes.createInput(profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeInput.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(ValueInput.createByReal(0.3)), adsk.fusion.ExtentDirections.NegativeExtentDirection)
        extrudeInput.startExtent = adsk.fusion.OffsetStartDefinition.create(ValueInput.createByReal(self.totalHeight))

        extrudes.add(extrudeInput)

        knobSketch.createDimensionedCircle(sketchOrigin, "1.25mm")

        profile = knobSketch.findInnermostProfile()
        extrudes.addSimple(profile, adsk.core.ValueInput.createByReal(self.totalHeight), adsk.fusion.FeatureOperations.CutFeatureOperation)

    def createTop(self):
        knobSketch = self.createKnobSketch()
        extrudes = self.component.features.extrudeFeatures
        profile = knobSketch.findProfileContainingPoint(Point3D.create(0, self.diameter/2 * 0.7, 0))
        self.topProfile = profile
        if not profile: raise ValueError("Knob profile not found")

        extrudeInput = extrudes.createInput(profile, FeatureOperations.JoinFeatureOperation)
        extrudeInput.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(ValueInput.createByReal(self.thickness)), adsk.fusion.ExtentDirections.PositiveExtentDirection)
        extrudeInput.startExtent = adsk.fusion.OffsetStartDefinition.create(ValueInput.createByReal(self.height))

        extrudes.add(extrudeInput)
        

    def createStem(self):
        extrudes = self.component.features.extrudeFeatures
        profile = self.knobSketch.findProfileContainingPoint(self.knobSketch.originSketchPoint.geometry)
        self.stemProfile = profile

        extrudes.addSimple(profile, ValueInput.createByReal(self.totalHeight), FeatureOperations.JoinFeatureOperation)
        
    def createGrips(self):
        if not self.topProfile: raise ValueError("No top profile set")    
        if not self.stemProfile: raise ValueError("No stem profile set")    

        allProfiles = self.knobSketch.sketch.profiles
        excludedProfiles = [self.topProfile, self.stemProfile]
        gripProfiles = adsk.core.ObjectCollection.create()
        for i in range(allProfiles.count):
            if not allProfiles.item(i) in excludedProfiles:
                gripProfiles.add(allProfiles.item(i))

        
        extrudes = self.component.features.extrudeFeatures
        extrudeInput = extrudes.createInput(gripProfiles, FeatureOperations.JoinFeatureOperation)
        extrudeInput.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(ValueInput.createByReal(self.thickness - 0.2)), adsk.fusion.ExtentDirections.PositiveExtentDirection)
        extrudeInput.startExtent = adsk.fusion.OffsetStartDefinition.create(ValueInput.createByReal(self.height + 0.1))

        extrudes.add(extrudeInput)


    ## Sketches
    def createKnobSketch(self):
        diameter = unitsMgr.evaluateExpression(self.diameterExpression)
        knobSketch = self.createSketch(self.component.xYConstructionPlane, "Knob Face Sketch")
        outerCircle = knobSketch.createDimensionedCircle(knobSketch.originSketchPoint, self.diameterExpression + '/2')
        innerCircle = knobSketch.createDimensionedCircle(knobSketch.originSketchPoint, self.diameterExpression + '/2 * 0.6')
        
        sketchArcs = knobSketch.sketch.sketchCurves.sketchArcs
        arcCenter = Point3D.create(0, diameter, 0)
        side = Point3D.create(diameter * 0.1, diameter + 0.01, 0)
        nubArc = sketchArcs.addByCenterStartSweep(arcCenter, side, math.pi/2)


        constraints = knobSketch.sketch.geometricConstraints

        #constraints.addCoincident(nubArc.centerSketchPoint, outerCircle)
        constraints.addCoincident(nubArc.startSketchPoint, outerCircle)
        constraints.addCoincident(nubArc.endSketchPoint, outerCircle)
        width = knobSketch.dimensions.addDistanceDimension(nubArc.startSketchPoint, nubArc.endSketchPoint, adsk.fusion.DimensionOrientations.AlignedDimensionOrientation, MachineSketch.createRandomAnglePoint(arcCenter))
        width.parameter.expression = '3 mm'

                
        patternInput = constraints.createCircularPatternInput([nubArc], knobSketch.originSketchPoint)
        patternInput.quantity = adsk.core.ValueInput.createByString(f'ceil( PI * {self.diameterExpression} / 6 mm)')
        constraints.addCircularPattern(patternInput)

        self.knobSketch = knobSketch
        return knobSketch
        
    
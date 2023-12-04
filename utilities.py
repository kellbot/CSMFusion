import adsk.core, adsk.fusion, adsk.cam, traceback, math, types
from adsk.core import Point3D, ValueInput
from adsk.fusion import UserParameter, SketchPoint, FeatureOperations

app = adsk.core.Application.get()
ui = app.userInterface

product = app.activeProduct
design = adsk.fusion.Design.cast(product)
unitsMgr = design.unitsManager
root = design.rootComponent

shellSpacing = 1.3

# default design units are CM unless explicitly specified or used in a Parameter
zAxis = design.rootComponent.zConstructionAxis

# Some utilities

class UserParameters:
    
    drumDiameter: adsk.fusion.UserParameter
    drumRadius: adsk.fusion.UserParameter
    
    needleCount: adsk.fusion.UserParameter
    needleSlotDepth: adsk.fusion.UserParameter
    needleSlotWidth: adsk.fusion.UserParameter
    yarnSlotWidth: adsk.fusion.UserParameter

    @staticmethod
    def set(name: str, value: [int, float, str], units: str = None):
        try:
            # Check to see if it already exists
            if parameter:= UserParameters.findByName(name):
                if units: 
                    parameter.expression = str(value) + units
                else: 
                    parameter.value = value
            # Otherwise create it
            else:      
                if units is None: units = ''
                input = adsk.core.ValueInput.createByString(str(value) + units)     
                parameter = design.userParameters.add(name, input, units, 'Created by CSM Generator')
            setattr(UserParameters, name, parameter)
        except ValueError as e:
            ui.messageBox(e)


    @staticmethod
    def findByName(name: str):
        userParameters = design.userParameters

        for parameter in userParameters:
            if parameter.name == name:
                return parameter

        return False

# Classes which make manipulating sketches less vebose
class SketchCommandBase:
    
    def __init__(self, sketch: adsk.fusion.Sketch):
        self.sketch = sketch
        self.sketchLines = sketch.sketchCurves.sketchLines
        self.dims = adsk.fusion.SketchDimensions.cast(self.sketch.sketchDimensions)


    def createDimensionedCircle(self, center, dimensionExpression: [str]):
        sketch = self.sketch
        radius = unitsMgr.evaluateExpression(dimensionExpression)
        circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(center, radius)

        textPoint = createShiftedPoint(center, 0.1)
        dim = self.dims.addRadialDimension(circle, textPoint)
        dim.parameter.expression = dimensionExpression
        return circle
    
    def createDimensionedCenterPointRectangle(self, center: Point3D, dimensionX: [UserParameter, int, float], dimensionY: [UserParameter, int, float]):
        if dimensionX is str or dimensionY is str:
            raise ValueError("String provided as dimension")
        xDimValue = dimensionX.value if isinstance(dimensionX, UserParameter) else dimensionX
        yDimValue = dimensionY.value if  isinstance(dimensionY, UserParameter)  else dimensionY
     
        pointA = adsk.core.Point3D.create(center.x - xDimValue/2, center.y - yDimValue/2, 0)
        lines  = self.sketchLines.addCenterPointRectangle(center, pointA)  
        line1 = lines.item(0)
        line2 = lines.item(1)

        textPoint = createShiftedPoint(center, 0.1)
        textPoint2 = createShiftedPoint(center, 0.1)
        dimX = self.dims.addDistanceDimension(line1.startSketchPoint, line1.endSketchPoint, adsk.fusion.DimensionOrientations.AlignedDimensionOrientation, textPoint )
        dimY = self.dims.addDistanceDimension(line2.startSketchPoint, line2.endSketchPoint, adsk.fusion.DimensionOrientations.AlignedDimensionOrientation, textPoint2 )

        dimX.parameter.expression = dimensionX.expression if  isinstance(dimensionX, UserParameter) else f'{dimensionX} cm'
        dimY.parameter.expression = dimensionY.expression if  isinstance(dimensionY, UserParameter) else f'{dimensionY} cm'

        for i in range(lines.count):
            app.log(str(i))
            if i == lines.count-1: 
                pass
            else:
               self.sketch.geometricConstraints.addPerpendicular(lines.item(i), lines.item(i+1))

        return lines




def createNewComponent():
    # Get the active design.
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)

    rootComp = design.rootComponent
    allOccs = rootComp.occurrences
    newOcc = allOccs.addNewComponent(adsk.core.Matrix3D.create())
    return newOcc




# Adds a two dimension chamfer to the end interior loop of an extrusion
def chamferExtrusion(extrude, horizontal, vertical):
    # chamfer the top edge
    extrudeEndFace = extrude.endFaces.item(0)
    brepLoops = extrudeEndFace.loops
    innerLoop = brepLoops.item(0)
    if innerLoop.isOuter:
         innerLoop = brepLoops.item(1)
    brepEdges = innerLoop.edges
    brepEdge = brepEdges.item(0)
    edgeCollection = adsk.core.ObjectCollection.create()
    edgeCollection.add(brepEdge)

    # Create the ChamferInput object.
    chamfers = design.rootComponent.features.chamferFeatures
    input = chamfers.createInput2() 
    horizontalOffset = adsk.core.ValueInput.createByReal(horizontal)   
    verticalOffset = adsk.core.ValueInput.createByReal(vertical)   

    input.chamferEdgeSets.addTwoDistancesChamferEdgeSet(edgeCollection, horizontalOffset, verticalOffset, False, False)
    
    # Create the chamfer.
    return chamfers.add(input)     

## Drawing

# Create a polygon in a sketch
def drawPolygon(sketch: adsk.fusion.Sketch, center_point: Point3D, num_sides: int, distance: float):
    try:
        if num_sides < 3:
            raise ValueError("Number of sides must be 3 or greater.")

        # Calculate the angle between each vertex
        angle_offset = 2 * math.pi / num_sides

        # Calculate the coordinates of the polygon vertices
        vertices = [
            adsk.core.Point3D.create(center_point.x + distance * math.cos(angle_offset * i),
                                     center_point.y + distance * math.sin(angle_offset * i),
                                     center_point.z)
            for i in range(num_sides)
        ]

        # Create sketch lines to form the polygon
        lines = sketch.sketchCurves.sketchLines
        for i in range(num_sides):
            start_point = vertices[i]
            end_point = vertices[(i + 1) % num_sides]  # Connect the last vertex to the first one
            lines.addByTwoPoints(start_point, end_point)

    except Exception as e:
        ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Creates a 360 degree circular pattern
def circularPattern(featureCollection: adsk.core.ObjectCollection, quantity: int, angle: int = 360):
    
    firstFeature = featureCollection.item(0)

    # Create the input for circular pattern
    circularFeats = firstFeature.parentComponent.features.circularPatternFeatures
    circularFeatInput = circularFeats.createInput(featureCollection, zAxis)
    
    # Set the quantity of the elements
    circularFeatInput.quantity = adsk.core.ValueInput.createByReal(quantity)
    
    # Set the angle of the circular pattern
    circularFeatInput.totalAngle = adsk.core.ValueInput.createByString( str(angle) + ' deg')
    
    # Set symmetry of the circular pattern
    circularFeatInput.isSymmetric = False
    
    # Set compute type
    #circularFeatInput.patternComputeOption = adsk.fusion.PatternComputeOptions.OptimizedPatternCompute

    # Create the circular pattern
    return circularFeats.add(circularFeatInput)

def getAllSketchProfiles(sketch):
    profs = adsk.core.ObjectCollection.create()
    for prof in sketch.profiles:
        profs.add(prof)
    return profs

def findProfileContainingPoint(sketch, point: adsk.core.Point3D):
    try:
        # Iterate through sketch profiles
        for profile in sketch.profiles:
            # Check if the origin is inside the profil
                if is_point_inside_profile(point, profile):
                    return profile

        # Return None if no profile contains the origin
        return None

    except Exception as e:
        ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
        return None
    
# really only checks the bounding box    
def is_point_inside_profile(point: adsk.core.Point3D, profile: adsk.fusion.Profile):
    return profile.boundingBox.minPoint.x <= point.x <= profile.boundingBox.maxPoint.x and profile.boundingBox.minPoint.y <= point.y <=profile.boundingBox.maxPoint.y

#only goes through origin
def createSketchAtAngle(existing_plane: adsk.fusion.ConstructionPlane, angle_degrees: float) -> adsk.fusion.Sketch:
    try:
        planes = existing_plane.component.constructionPlanes
        planeInput = planes.createInput()
         
        angle = adsk.core.ValueInput.createByString(str(angle_degrees) + 'deg')
        planeInput.setByAngle(design.rootComponent.zConstructionAxis,  angle, existing_plane)
        newPlane = planes.add(planeInput)
        newSketch = existing_plane.component.sketches.add(newPlane)
        return newSketch

    except Exception as e:
        ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
        return None

# I feel like there's probably already something in the API that does this but I can't find it
# Note: this doesn't do anything to validate units, so god help you there    
def createPointByOffset(originalPoint: Point3D, offset: dict) -> Point3D:
    try: 
        if (len(offset) != 3):
            raise ValueError(f"Offset should be a dictionary of 3 values for x, y, and z")
        return Point3D.create(originalPoint.x + offset["x"], originalPoint.y + offset["y"], originalPoint.z + offset["z"])    

    except ValueError as e:
        ui.messageBox('Failed:\n{}'.format(e))
        return None
    
def createShiftedPoint(point: Point3D, distance: float):
    oldPoint = point.geometry if  isinstance(point, SketchPoint) else point
    shiftPoint = Point3D.create(oldPoint.x, oldPoint.y, oldPoint.z)
    shiftPoint.x += distance
    shiftPoint.y += distance
    return shiftPoint
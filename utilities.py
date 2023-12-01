import adsk.core, adsk.fusion, adsk.cam, traceback, math
from adsk.core import Point3D

app = adsk.core.Application.get()
ui = app.userInterface

product = app.activeProduct
design = adsk.fusion.Design.cast(product)


zAxis = design.rootComponent.zConstructionAxis

# Some utilities

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
def circularPattern(featureCollection, quantity):
    
    firstFeature = featureCollection.item(0)

    # Create the input for circular pattern
    circularFeats = firstFeature.parentComponent.features.circularPatternFeatures
    circularFeatInput = circularFeats.createInput(featureCollection, zAxis)
    
    # Set the quantity of the elements
    circularFeatInput.quantity = adsk.core.ValueInput.createByReal(quantity)
    
    # Set the angle of the circular pattern
    circularFeatInput.totalAngle = adsk.core.ValueInput.createByString('360 deg')
    
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
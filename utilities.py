import adsk.core, adsk.fusion, adsk.cam, traceback, math


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

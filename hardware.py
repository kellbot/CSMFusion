import adsk.core, adsk.fusion, adsk.cam, traceback, math
from adsk.core import Point3D, ValueInput
from adsk.fusion import FeatureOperations
from .utilities import *

app = adsk.core.Application.get()
ui = app.userInterface

product = app.activeProduct
design = adsk.fusion.Design.cast(product)

# Adds the ability to createa  cutout for a metric nut at a given point on a component
def createM3NutCutout(plane: adsk.fusion.BRepFace, center: Point3D, flipDirection:bool = False)->bool:
    comp = plane.body.parentComponent
    sketch = comp.sketches.add(plane)
    drawPolygon(sketch, center, 6, 0.635/2)
    direction = 1
    if (flipDirection): direction = direction * -1
    comp.features.extrudeFeatures.addSimple(sketch.profiles.item(0), ValueInput.createByReal(0.3 * direction), FeatureOperations.CutFeatureOperation )
    return True

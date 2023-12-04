import adsk.core, adsk.fusion, adsk.cam, random
from .utilities import *
from typing import Any
from enum import Enum

class ReferencePointType(Enum):
	Center = 1
	Corner = 2

class MachineSketch():
	sketch: adsk.fusion.Sketch
	dimensions: adsk.fusion.SketchDimensions
	sketchLines: adsk.fusion.SketchLines

	# Creates a new sketch on the given component and names it
	def __init__(self, component: adsk.fusion.Component, referencePlane: adsk.core.Base, name: str = None) -> None:
		sketch = component.sketches.add(referencePlane)
		if name: 
			sketch.name = name
		self.dimensions =  adsk.fusion.SketchDimensions.cast(sketch.sketchDimensions)
		self.sketchLines = sketch.sketchCurves.sketchLines

		self.sketch = sketch
	   
	def createDimensionedCircle(self, center, dimensionExpression: [str]):
		sketch = self.sketch
		radius = unitsMgr.evaluateExpression(dimensionExpression)
		# create sketchPoint if needed
		if isinstance(center, Point3D):
			center = self.sketch.sketchPoints.add(center)

		circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(center, radius)

		textPoint = MachineSketch.createRandomAnglePoint(center)
		dim = self.dimensions.addRadialDimension(circle, textPoint)
		dim.parameter.expression = dimensionExpression
		return circle
	
	# creates a rectangle and sets the constraints
	def createDimensionedRectangle(self, referencePoint: [Point3D, SketchPoint], xDimensionExpression: str, yDimensionExpression: str, referenceType: ReferencePointType = ReferencePointType.Corner):
		
		# evaluate dimensions
		width = unitsMgr.evaluateExpression(xDimensionExpression)
		height = unitsMgr.evaluateExpression(yDimensionExpression)
		
		# create sketchPoint if needed
		if isinstance(referencePoint, Point3D):
			referencePoint = self.sketch.sketchPoints.add(referencePoint)
		if referenceType == ReferencePointType.Corner:
			point1 = referencePoint
			point2 = self.sketch.sketchPoints.add(MachineSketch.createShiftedPoint(referencePoint, width, height, 0))
			rectangleLines = self.sketchLines.addTwoPointRectangle(point1, point2)
			[line1, line2] = [rectangleLines.item(0), rectangleLines.item(1)]
			dimX = self.dimensions.addDistanceDimension(line1.startSketchPoint, line1.endSketchPoint, adsk.fusion.DimensionOrientations.AlignedDimensionOrientation, MachineSketch.createRandomAnglePoint(referencePoint) )
			dimY = self.dimensions.addDistanceDimension(line2.startSketchPoint, line2.endSketchPoint, adsk.fusion.DimensionOrientations.AlignedDimensionOrientation, MachineSketch.createRandomAnglePoint(referencePoint))

			dimX.parameter.expression = xDimensionExpression
			dimY.parameter.expression = yDimensionExpression

			# make them perpendicular to each other
			for i in range(rectangleLines.count):
				if i == rectangleLines.count-1: 
					pass
				else:
					self.sketch.geometricConstraints.addPerpendicular(rectangleLines.item(i), rectangleLines.item(i+1))


		
		else:
			raise Exception("Sorry, that hasn't been implemented yet")
		return rectangleLines
		
	def findProfileContainingPoint(self, point):

		# Iterate through sketch profiles
		for profile in self.sketch.profiles:
			# Check if the origin is inside the profil
				if is_point_inside_profile(point, profile):
					return profile

		# Return None if no profile contains the origin
		return None



	@staticmethod
	def createShiftedPoint(point, x, y, z):
		oldPoint = point.geometry if isinstance(point, SketchPoint) else point
		newPoint = Point3D.create(oldPoint.x, oldPoint.y, oldPoint.z)
		newPoint.x += x
		newPoint.y += y
		newPoint.z += z
		return newPoint
	
	# this creates a new point at a random angle from the location, for placing dimension text
	@staticmethod
	def createRandomAnglePoint(location: [Point3D, SketchPoint]) -> Point3D:

		# if it's a sketch point we need to fetch the geometry
		oldPoint = location.geometry if  isinstance(location, SketchPoint) else location

		shiftPoint = Point3D.create(oldPoint.x, oldPoint.y, oldPoint.z)
		shiftPoint.x += random.uniform(-1, 1)
		shiftPoint.y += random.uniform(-1, 1)
		
		return shiftPoint
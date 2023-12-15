import adsk.core, adsk.fusion, adsk.cam, random
from .utilities import *
from typing import Any
from enum import Enum
from adsk.fusion import UserParameter

class ReferencePointType(Enum):
	Center = 1
	Corner = 2

class MachineSketch():
	sketch: adsk.fusion.Sketch
	dimensions: adsk.fusion.SketchDimensions
	sketchLines: adsk.fusion.SketchLines
	originSketchPoint: adsk.fusion.SketchPoint

	# Creates a new sketch on the given component and names it
	def __init__(self, component: adsk.fusion.Component, referencePlane: adsk.core.Base, name: str = None) -> None:
		sketch = component.sketches.add(referencePlane)
		if name: 
			sketch.name = name
		self.dimensions =  adsk.fusion.SketchDimensions.cast(sketch.sketchDimensions)
		self.sketchLines = sketch.sketchCurves.sketchLines

		self.sketch = sketch
		self.originSketchPoint = sketch.sketchPoints.add(origin)
		self.originSketchPoint.isFixed = True
	   
	def createDimensionedCircle(self, center, dimensionExpression: [str]):
		sketch = self.sketch
		radius = unitsMgr.evaluateExpression(dimensionExpression)
		# create sketchPoint if needed
		if isinstance(center, Point3D):
			circleCenter = self.sketch.sketchPoints.add(center)
		else: 
			circleCenter = center

		circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(circleCenter, radius)

		textPoint = MachineSketch.createRandomAnglePoint(circleCenter)
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

	def findInnermostProfile(self):

		point = adsk.core.Point3D.create(0,0,0)
		# Iterate through sketch profiles
		for profile in self.sketch.profiles:
			# Check if the origin is inside the profile
			if is_point_inside_profile(point, profile):
				# if it has more than one profileLoop then it's not the one we want
				if profile.profileLoops.count == 1:
					return profile


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
	

class MachineParameters:
	
	# Input Parameters: These are things that are available for editing in the final design
	drumDiameter: UserParameter	# The diameter of the needle cylinder
	needleCount: UserParameter  # The number of needles on the cylinder
	rampAngle: UserParameter	# Legit no idea what this is

	# Other things we need to define as user parameters, for reference
	drumRadius: UserParameter   	# Convenience parameter
	shellDiameter: UserParameter
	shellRadius: UserParameter
	ramp: UserParameter				# unclear
	
	needleSlotDepth: UserParameter  # How deep the needles are set in the cylinder. This is related to the needle selector depth
	needleSlotWidth: UserParameter	# How wide the slot for the needle is. This is related to the needle width
	yarnSlotWidth: UserParameter	# The top of the slot, which the yarn is drawn into
	camSize: UserParameter			# This is the width, in degrees, of the cam. It is based on the original scale of 15 degrees for a 120mm cylinder
	
	# Some Fixed Values, units in MM
	shellSpacing = 2.6
	shellThickness = 0.4


	def __init__(self) -> None:
		self.setUserParameter('needleCount', 134)
		self.setUserParameter('drumDiameter', 220, 'mm')
		self.setUserParameter('rampAngle', 53, 'deg')

		self.setUserParameter('drumRadius',  f'{self.drumDiameter.name} / 2', "mm")  
		self.setUserParameter('shellDiameter',  f'{self.drumDiameter.name} + {self.shellSpacing * 10}', "mm")  

		self.setUserParameter('shellRadius',  f'{self.shellDiameter.name} / 2', "mm")  
		self.setUserParameter('ramp', f'{self.rampAngle.name} * (120 mm / {self.drumDiameter.name}) - 3','deg')
		self.setUserParameter('camSize', f'(120 mm / {self.drumDiameter.name}) * 15', 'deg')


		self.setUserParameter('needleSlotDepth', 7.5, "mm" )
		self.setUserParameter('needleSlotWidth', 1.7, 'mm')
		self.setUserParameter('yarnSlotWidth', 3.6, 'mm')
		
	
	def setUserParameter(self, name: str, value: [int, float, str], units: str = None):
		try:
			# Check to see if it already exists
			if parameter:= MachineParameters.findUserParameterByName(name):
				if units: 
					parameter.expression = str(value) + units
				else: 
					parameter.value = value
			# Otherwise create it
			else:      
				if units is None: units = ''
				input = adsk.core.ValueInput.createByString(str(value) + units)     
				parameter = design.userParameters.add(name, input, units, 'Created by CSM Generator')
			setattr(self, name, parameter)
		except ValueError as e:
			ui.messageBox(e)
		except Exception as te:
			ui.messageBox('Invalid expression: ' + str(value) + units)
			app.log('Failed:\n{}'.format(traceback.format_exc()))


	@staticmethod
	def findUserParameterByName(name: str):
		userParameters = design.userParameters

		for parameter in userParameters:
			if parameter.name == name:
				return parameter

		return False


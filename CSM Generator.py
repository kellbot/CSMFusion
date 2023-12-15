#Author- Kelly Maguire
#Description-

import adsk.core, adsk.fusion, traceback

# these are done like this for path reasons I don't really understand
from .drum import createDrum 
from .shell import createShell
from .utilities import *
from .NeedleCam import NeedleCam
from .MainBase import MainBase
from .MachineComponent import Knob
from .MachineClasses import MachineParameters

params = MachineParameters()


def sideKnob(angle):
    knobMatrix = adsk.core.Matrix3D.create()

    knobMatrix.setToRotation(-math.pi / 2, design.rootComponent.yConstructionAxis.geometry.direction, origin)
    rotationMatrix = adsk.core.Matrix3D.create()
    rotationMatrix.setToRotation(angle, design.rootComponent.zConstructionAxis.geometry.direction, origin)

    knobMatrix.translation =  adsk.core.Vector3D.create(-params.shellRadius.value + .05, 0, 4.15)
    knobMatrix.transformBy(rotationMatrix)

    knob = Knob('6mm', '4mm', '20mm', 'Knob 1', False, knobMatrix)
    knobCollection = adsk.core.ObjectCollection.create()
    knobCollection.add(knob.component)

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()

        # createDrum()
        # createShell()
        # needleCam = NeedleCam()

        # sideKnob(params.camSize.value)
        # sideKnob(-params.camSize.value)
        
        MainBase()

        design.activateRootComponent()

    except:
       app.log('Failed:\n{}'.format(traceback.format_exc()))

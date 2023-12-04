import adsk.core, adsk.fusion, adsk.cam, traceback
from .utilities import *
from .MachineClasses import MachineSketch
from typing import Dict

origin = Point3D.create(0,0,0)

class MachineComponent():
    component: adsk.fusion.Component

    machineSketches: Dict[str, MachineSketch] = {}

    def __init__(self, design: adsk.fusion.Design, transform = None) -> None:
        if not transform:
            transform = adsk.core.Matrix3D.create()
        self.component = design.rootComponent.occurrences.addNewComponent(transform).component

    def createSketch(self, referencePlane: adsk.core.Base, name: str = None):
        newSketch = MachineSketch(self.component, referencePlane, name)
        self.machineSketches[name] = newSketch
        return newSketch
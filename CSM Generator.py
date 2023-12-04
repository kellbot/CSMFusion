#Author- Kelly Maguire
#Description-

import adsk.core, adsk.fusion, traceback

# these are done like this for path reasons I don't really understand
from .drum import createDrum 
from .shell import createShell
from .utilities import *
from .NeedleCam import NeedleCam

Params = UserParameters
def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()

        Params.set('needleCount', 134)
        Params.set('drumDiameter', 220, 'mm')
        Params.set('drumRadius',  f'{Params.drumDiameter.name} / 2', "mm")  
        Params.set('needleSlotDepth', 7.5, "mm" )
        Params.set('needleSlotWidth', 1.7, 'mm')
        Params.set('yarnSlotWidth', 3.6, 'mm')
        Params.set('camAngle', 59, 'deg')

        createDrum()
        createShell()
        needleCam = NeedleCam(design)

        design.activateRootComponent()

    except:
       app.log('Failed:\n{}'.format(traceback.format_exc()))

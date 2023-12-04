#Author- Kelly Maguire
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
from .drum import createDrum 
from .shell import createShell
from .utilities import *

app = adsk.core.Application.get()
ui  = app.userInterface
product = app.activeProduct
design = adsk.fusion.Design.cast(product)
#everything is in CM, which is terrible but I don't know how to change it

Params = UserParameters

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        #ui  = app.userInterface
        #try:
        Params.set('needleCount', 134)
        Params.set('drumDiameter', 220, 'mm')
        Params.set('drumRadius',  f'{Params.drumDiameter.name} / 2', "mm")  
        Params.set('needleSlotDepth', 7.5, "mm" )
        Params.set('needleSlotWidth', 1.7, 'mm')
        Params.set('yarnSlotWidth', 3.6, 'mm')
        # except:
        #     app.log("Failed to create some or all user parameters")
        #     app.log('Failed:\n{}'.format(traceback.format_exc()))

        createDrum()
        createShell()

        design.activateRootComponent()

    except:
       app.log('Failed:\n{}'.format(traceback.format_exc()))

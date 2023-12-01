#Author- Kelly Maguire
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
from .drum import createDrum 
from .shell import createShell

app = adsk.core.Application.get()
ui  = app.userInterface
product = app.activeProduct
design = adsk.fusion.Design.cast(product)
#everything is in CM, which is terrible but I don't know how to change it

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        #createDrum()
        createShell()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

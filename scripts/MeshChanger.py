import bge 

from Logging import Logging
from mathutils import Vector
import finder


class MeshChanger(object):
    def __init__(self,cont):
        self.log = Logging("MeshChanger","Debug")
        self.cont = cont
        self.own = cont.owner
        self.scene = bge.logic.getCurrentScene()
        
        self.msgSensor = self.cont.sensors["Message"]
        self.changeMesh = self.cont.actuators["ChangeMesh"]
        
        self.log.msg("Init Completed.")
        
    def update(self):
        if self.msgSensor.positive : 
            msg = self.msgSensor.bodies[self.msgSensor.subjects.index("ChangeMesh")]
            self.changeMesh.mesh = msg
            self.cont.activate(self.changeMesh)
        pass
    

def main():
    cont = bge.logic.getCurrentController()
    own = cont.owner
     
    if 'matrix.meshChanger' not in own:
        own['matrix.meshChanger'] = MeshChanger(cont)
    else:
        own['matrix.meshChanger'].update()
 
if bge.logic.getCurrentController().mode == 0:
    main() 
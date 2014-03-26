import bge 

from Logging import Logging
from mathutils import Vector
import finder
from Messages import Messages,Message


class MeshChanger(object):
    def __init__(self,cont):
        self.log = Logging("MeshChanger","Debug")
        self.cont = cont
        self.own = cont.owner
        self.scene = bge.logic.getCurrentScene()
        self.messages = Messages(self.cont,self)
        
        self.msgSensor = self.cont.sensors["Message"]
        self.changeMesh = self.cont.actuators["ChangeMesh"]
        #self.log.msg("idx %i mesh %i"%(self.own['idx'],self.own['srcDstFlow']))
        
        if self.own['srcDstFlow'] == 0:
            self.mesh = "GreenPkt"
            self.changemesh()
            
        if self.own['srcDstFlow'] == 1:
            self.mesh = "BluePkt"
            self.changemesh()
        #self.log.msg("Init Completed.")
        
    def update(self):
        self.messages.update()
        try:
            #self.log.msg("idx %i mesh %i"%(self.own['idx'],self.own['srcDstFlow']))
            pass
        except KeyError:
            pass
        
    def changemesh(self):
        self.changeMesh.mesh = self.mesh
        self.cont.activate(self.changeMesh)   

def main():
    cont = bge.logic.getCurrentController()
    own = cont.owner
     
    if 'matrix.meshChanger' not in own:
        own['matrix.meshChanger'] = MeshChanger(cont)
    else:
        own['matrix.meshChanger'].update()
 
if bge.logic.getCurrentController().mode == 0:
    main() 
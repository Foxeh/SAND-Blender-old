import bge 

from Logging import Logging
from mathutils import Vector
import finder
from Messages import Messages,Message


class NodeMeshChanger(object):
    def __init__(self,cont):
        self.log = Logging("NodeMeshChanger","Debug")
        self.cont = cont
        self.own = cont.owner
        self.scene = bge.logic.getCurrentScene()
        self.messages = Messages(self.cont,self)
        
        self.msgSensor = self.cont.sensors["Message"]
        self.changeMesh = self.cont.actuators["ChangeMesh"]

        self.mesh = "WhiteNde"
        self.changemesh()

        
    def update(self):
        self.messages.update()

    def changenodemesh(self,msg):
        if self.own['ip'] == msg['source']:
           #0 = green, 1 = blue, 2 = yellow
           if msg['srcDstFlow'] ==  0 and self.mesh != "GreenNde":
               self.mesh = "GreenNde"
           if msg['srcDstFlow'] ==  1 and self.mesh != "BlueNde":
               self.mesh = "BlueNde"    
           if msg['srcDstFlow'] ==  2 and self.mesh != "YellowNde":
               self.mesh = "YellowNde" 
           self.changemesh()
               
               
               
    def changemesh(self):
        self.changeMesh.mesh = self.mesh
        self.cont.activate(self.changeMesh)   

def main():
    cont = bge.logic.getCurrentController()
    own = cont.owner
     
    if 'matrix.nodeMeshChanger' not in own:
        own['matrix.nodeMeshChanger'] = NodeMeshChanger(cont)
    else:
        own['matrix.nodeMeshChanger'].update()
 
if bge.logic.getCurrentController().mode == 0:
    main() 
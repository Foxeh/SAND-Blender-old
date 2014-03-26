import bge 

from Logging import Logging
from Messages import Messages
from mathutils import Vector
import finder

'''
Important
===========================================================
Must have an Always Sensor (,,,) to fire off the __init__

'''
class Node(object):
    def __init__(self,cont):
        self.log = Logging("Node","Debug")
        self.cont = cont
        self.own = cont.owner
        self.scene = bge.logic.getCurrentScene()
        self.messages = Messages(self.cont,self)
        
        #this is the packet object to spawn.
        self.packet = finder.findObjects(finder.byNameContains, ["Packet"], None, "objectsInactive")[0]
        #this is the add packet actuator
        self.addPacket = self.cont.actuators['AddPacket']
        self.addPacket.object = self.packet
        
        self.log.msg("Init Completed.")
        
    def update(self):
        #self.log.msg("update")
        self.messages.update()

    def addpacket(self,msg):
        if self.own.parent['ip'] == msg['source']:                   
            packetSteering = self.packet.actuators["Steering"]
            targets = finder.findObjects(finder.byProperty,['ip'],"Game")
            #self.log.msg(targets)
            for target in targets:
                if target['ip'] == msg['dest']:
                    packetSteering.target = target 
                    self.cont.activate(self.addPacket)
    

def main():
    cont = bge.logic.getCurrentController()
    own = cont.owner

    if 'matrix.node' not in own:
        own['matrix.node'] = Node(cont)
    else:
        own['matrix.node'].update()
 
if bge.logic.getCurrentController().mode == 0:
    main() 
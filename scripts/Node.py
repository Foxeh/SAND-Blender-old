import bge 
import GameLogic
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
        #self.addPacket = self.cont.actuators['AddPacket']
        #self.addPacket.object = self.packet
        self.packets = {}
        self.packetIdx = 0
        self.log.msg("Init Completed.")
        
    def update(self):
        self.messages.update()

    def addpacket(self,msg):
        if self.own.parent['ip'] == msg['source']:                   
            packet = self.createPacket(msg)
            packet['source'] = msg['source']
            packet['dest'] = msg['dest']
            packet['srcDstFlow'] = msg['srcDstFlow']
            packet['idx'] = self.packetIdx
            self.packetIdx = self.packetIdx + 1
            
    def createPacket(self,msg):
        packetSteering = self.packet.actuators["Steering"]
        targets = GameLogic.globalDict["matrix.nodes"]
        target = targets[msg['dest']]          
        packetSteering.target = target 
        #self.cont.activate(self.addPacket) 
        return self.scene.addObject(self.packet, self.own,0) 
        #return self.addPacket.objectLastCreated  
        #return self.addPacket.instantAddObject()

def main():
    cont = bge.logic.getCurrentController()
    own = cont.owner

    if 'matrix.node' not in own:
        own['matrix.node'] = Node(cont)
    else:
        own['matrix.node'].update()
 
if bge.logic.getCurrentController().mode == 0:
    main() 
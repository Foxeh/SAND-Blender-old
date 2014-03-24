#import bge 

from Logging import Logging
from mathutils import Vector
from random import randint
import finder
from Messages import Messages, Message

class NodeSpawner(object):
    def __init__(self,cont):
        self.log = Logging("NodeSpawner","Debug")
        self.cont = cont
        self.own = cont.owner
        self.scene = bge.logic.getCurrentScene()
        
        self.messages = Messages(self.cont,self)
        
        #this is the packet object to spawn.
        self.Node = finder.findObjects(finder.byNameContains, ["Node"], None, "objectsInactive")[0]
        #this is the add packet actuator
        self.addNode = self.cont.actuators['AddNode']
        self.radar = self.cont.sensors["Radar"]
        
        self.addNode.object = self.Node
        
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        
        self.nodes = {}
        
        
        self.kbd = self.cont.sensors['Keyboard']
        self.kbd1 = self.cont.sensors['Keyboard1']
        
        self.log.msg("Init Completed.")
    
    def networkdata(self,data):
        #this is called by the message handler
        self.log.msg(dir(data))
        
        
    def createNode(self):
        #objectLastCreated
        self.cont.activate(self.addNode)
        
            
    def update(self):

        self.messages.update()

        if self.kbd1.positive:
            #self.log.msg("Pressed add packet")
            msg = Message("addpacket",{'derp':1})
            self.messages.send(msg)
            #bge.logic.sendMessage("addpacket", "1") 
            
        if self.kbd.positive:
            #self.log.msg("Pressed add node")
            #if self.radar.positive:
            #self.log.msg("PRadar pos")
            self.x = self.x + randint(-32,60)
            self.y = self.y + randint(-32,60)
            vec = Vector((self.x,self.y,self.z))
            self.own.localPosition = vec          
            self.createNode()
          
        pass
    

def main():
    cont = bge.logic.getCurrentController()
    own = cont.owner
     
    if 'matrix.nodeSpawner' not in own:
        own['matrix.nodeSpawner'] = NodeSpawner(cont)
    else:
        own['matrix.nodeSpawner'].update()
 
if bge.logic.getCurrentController().mode == 0:
    main() 
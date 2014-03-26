#import bge 

from Logging import Logging
from mathutils import Vector
from random import randint
import finder
from Messages import Messages, Message

import GameLogic

class NodeSpawner(object):
    def __init__(self,cont):
        self.log = Logging("NodeSpawner","Debug")
        self.cont = cont
        self.own = cont.owner
        self.scene = bge.logic.getCurrentScene()
        
        self.messages = Messages(self.cont,self)
        
        #this is the packet object to spawn.
        self.Node = finder.findObjects(finder.byNameContains, ["Node"], None, "objectsInactive")[0]
        #self.packet = finder.findObjects(finder.byNameContains, ["Packet"], None, "objectsInactive")[0]

        
        #this is the add packet actuator
        #self.addNode = self.cont.actuators['AddNode']
        self.radar = self.cont.sensors["Radar"]
        
        #self.addNode.object = self.Node
        
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        
        GameLogic.globalDict["matrix.nodes"] = self.nodes = {}
        
        
        self.log.msg("Init Completed.")
    
    def networkdata(self,data):
        #this is called by the message handler
        if data['source'] not in self.nodes:
            self.x = randint(-120,120)
            self.y = randint(-120,120)
            vec = Vector((self.x,self.y,self.z))
            self.own.localPosition = vec          
            self.nodes[data['source']] = self.createNode()
            self.nodes[data['source']]['ip'] = data['source']           
            self.log.msg("Adding Source Node %i"%data['source'])
            
        if data['dest'] not in self.nodes:
            self.x = randint(-120,120)
            self.y = randint(-120,120)
            vec = Vector((self.x,self.y,self.z))
            self.own.localPosition = vec          
            self.nodes[data['dest']] = self.createNode()
            self.nodes[data['dest']]['ip'] = data['dest']
            self.log.msg("Adding Dest Node %i"%data['dest'])
        
        msg = Message("addpacket",{'dest':data['dest'], 'source':data['source'],'srcDstFlow':data['srcDstFlow']})
        self.messages.send(msg)
        
        msg = Message("changenodemesh",{'dest':data['dest'], 'source':data['source'],'srcDstFlow':data['srcDstFlow']})
        self.messages.send(msg)
        
        #if data['srcDstFlow'] == 0:
        #    self.log.msg("Mesh Change to Green")           
        #    msg = Message("changemesh",{'mesh':'GreenPkt'})
        #
        #    self.messages.send(msg)
                    
        
        
    def createNode(self):
        #objectLastCreated
        #self.cont.activate(self.addNode)
        #return self.addNode.objectLastCreated
        return self.scene.addObject(self.Node, self.own,0) 
        
            
    def update(self):

        self.messages.update()
'''
        if self.kbd1.positive:
            #self.log.msg("Pressed add packet")
            msg = Message("addpacket",{'derp':1})
            self.messages.send(msg)
            #bge.logic.sendMessage("addpacket", "1") 
            
        if self.kbd.positive:
            #self.log.msg("Pressed add node")
            #if self.radar.positive:
            #self.log.msg("PRadar pos")

 '''         
    

def main():
    cont = bge.logic.getCurrentController()
    own = cont.owner
     
    if 'matrix.nodeSpawner' not in own:
        own['matrix.nodeSpawner'] = NodeSpawner(cont)
    else:
        own['matrix.nodeSpawner'].update()
 
if bge.logic.getCurrentController().mode == 0:
    main() 
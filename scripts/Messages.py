'''
This is a message handling class for use by all objects in the game.

bge.logic.sendMessage(subject, body, to, from)

'''
from Logging import Logging
from bge import logic
import json

class Message(object):
    def __init__(self,subject,payload='',sender='',receiver=''):
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.payload = payload
    
             
class Messages(object):
    def __init__(self,cont,parent):
        self.cont = cont
        self.own = cont.owner
        self.parent = parent
        self.log = Logging("Messages","Debug")
        self.canRecv = True
        try:
            self.msgSensor = self.cont.sensors["Message"]
        except KeyError:
            self.canRecv = False
        
    def update(self):
        if self.canRecv:
            self._handleMessage()
            
    
    def send(self,msg):       
        logic.sendMessage(msg.subject,json.dumps(msg.payload), msg.receiver,msg.sender) 

        
    def _handleMessage(self):

        if self.msgSensor.positive:  
            #self.log.msg("Got Message!")
            for subject in self.msgSensor.subjects:
                f = None
                try:
                    f = getattr(self.parent,subject.lower())
                except AttributeError:
                    pass
                
                if f:
                    #TODO: need to define the msg protocol
                    payload = json.loads(self.msgSensor.bodies[self.msgSensor.subjects.index(subject)])
                    f(payload)
                else:
                    #self.log.msg("Missing function for %s"%(subject))
                    pass
                
                
                
                
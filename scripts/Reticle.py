import bge 

from Logging import Logging
from Messages import Messages, Message

class Reticle(object):
    def __init__(self,cont):
        self.log = Logging("Reticle","Debug")
        self.cont = cont
        self.own = cont.owner
        self.scene = bge.logic.getCurrentScene()
        self.messages = Messages(self.cont,self)  
        
        self.ray = self.cont.sensors["Ray"]
               
        self.log.msg("Init Completed.")    
        
    def update(self):
        self.messages.update() 
        if self.ray.positive:
            bge.render.drawLine(self.own.worldPosition,self.ray.hitPosition,[255,30,30]) 
            hitObj = self.ray.hitObject
            try:
                msg = Message("statusupdate",{'ip':hitObj['ip']})
                self.messages.send(msg)   
            except KeyError:
                pass

def main():
    cont = bge.logic.getCurrentController()
    own = cont.owner

    if 'matrix.reticle' not in own:
        own['matrix.reticle'] = Reticle(cont)
    else:
        own['matrix.reticle'].update()
 
if bge.logic.getCurrentController().mode == 0:
    main() 
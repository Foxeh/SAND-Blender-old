import bge 

from Logging import Logging
from Messages import Messages

class HUD(object):
    def __init__(self,cont):
        self.log = Logging("HUD","Debug")
        self.cont = cont
        self.own = cont.owner
        self.scene = bge.logic.getCurrentScene()
        self.status = self.scene.objects["Status"]
        self.status.text = "Nothing to see here"
        
        self.messages = Messages(self.cont,self)        
        self.log.msg("Init Completed.")    
        
    def update(self):
        self.messages.update() 
    
    def statusupdate(self,msg):
        self.status.text = "Object is a Node with IP of %s"%msg['ip']
def main():
    cont = bge.logic.getCurrentController()
    own = cont.owner

    if 'matrix.hud' not in own:
        own['matrix.hud'] = HUD(cont)
    else:
        own['matrix.hud'].update()
 
if bge.logic.getCurrentController().mode == 0:
    main() 
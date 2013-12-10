import bge

from Logging import Logging
    
class Splash(object):
    '''
    this class is the Splash
    '''
    def __init__(self,cont):
        self.cont = cont
        self.own = cont.owner
        self.log = Logging("Splash","Debug")
        self.scene = bge.logic.getCurrentScene()
        self.title = self.scene.objects["Title"]
        
        self.title.text = "SAND-Matrix"
        
        self.log.msg("Init complete.")
        
    def update(self):
        self._handleMessage()
        
    def _handleMessage(self):
        pass

    
def main():
    cont = bge.logic.getCurrentController()
    own = cont.owner
    
    if 'matrix.splash' not in own:
        own['matrix.splash'] = Splash(cont)
    else:
        own['matrix.splash'].update()

if bge.logic.getCurrentController().mode == 0:
    main() 
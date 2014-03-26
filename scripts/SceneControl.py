'''
This is the main scene controller

It is meant to handle all scene level control

This should be parented to an empty in the scene and hooked to an always logic
brick set to True Level Triggering (```) so the scene control update method fires.

'''
import bge
#import finder
from Networking import Networking
#from GunUdpListener import GunUdpListener
from Logging import Logging
    
class SceneControl(object):
    '''
    this class is the main entry point and control of the game scene
    '''
    def __init__(self,cont):
        self.cont = cont
        self.own = cont.owner
        self.scene = bge.logic.getCurrentScene()
        #stash ref to objects that need to be updated in the scene that do not have (or need) an Always brick
        self.sceneUpdates = []
        self.log = Logging("SceneControl","Debug")
        #set up network socket  
        
        self.cont.activate(self.own.actuators["HUD"])     
        
        self.sceneUpdates.append(Networking(self.cont))
        
        #self.sceneUpdates.append(GunUdpListener())
        #add the HUD
        
        #TODO: the player spawn doesn't work because of an issue with setting the active camera to the rig
        #spawn the player
        #bge.logic.sendMessage("PlayerSpawn", "", "PlayerSpawn", "SceneControl")
        #change the scene camera to the player rig
        #self.scene.active_camera =  self.scene.objects["FPS Camera"]
        
    def update(self):
        for o in self.sceneUpdates:
            o.update()
    
def main():
    cont = bge.logic.getCurrentController()
    own = cont.owner
    
    if 'matrix.sceneControl' not in own:
        own['matrix.sceneControl'] = SceneControl(cont)
    else:
        own['matrix.sceneControl'].update()

if bge.logic.getCurrentController().mode == 0:
    main() 
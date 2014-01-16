'''
This is the main scene controller

It is meant to handle all scene level control

This should be parented to an empty in the scene and hooked to an always logic
brick set to True Level Triggering (```) so the scene control update method fires.

'''
import bge
import finder
from Networking import Networking
from GunUdpListener import GunUdpListener
from Logging import Logging
    
class GameOver(object):
    '''
    this class is the main entry point and control of the game scene
    '''
    def __init__(self,cont):
        self.cont = cont
        self.own = cont.owner
        self.scene = bge.logic.getCurrentScene()
 
        self.log = Logging("GameOver","Debug")
        self.showScoreboard = self.cont.actuators['GoScoreboard']
        self.showScoreboard.scene="Scoreboard"
        self.kbd = self.cont.sensors['Keyboard']
        self.log.msg('init completed')
        
    def update(self):
        
        if self.kbd.positive:
            self.cont.activate(self.showScoreboard)
    
def main():
    cont = bge.logic.getCurrentController()
    own = cont.owner
    
    if 'matrix.gameover' not in own:
        own['matrix.gameover'] = GameOver(cont)
    else:
        own['matrix.gameover'].update()

if bge.logic.getCurrentController().mode == 0:
    main() 
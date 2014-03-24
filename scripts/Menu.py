'''
This is the main scene controller

It is meant to handle all scene level control

This should be parented to an empty in the scene and hooked to an always logic
brick set to True Level Triggering (```) so the scene control update method fires.

'''
import bge
from Logging import Logging
    
class Menu(object):
    '''
    this class is the main entry point and control of the game scene
    '''
    def __init__(self,cont):
        self.cont = cont
        self.own = cont.owner
        self.scene = bge.logic.getCurrentScene()
 
        self.log = Logging("Menu","Debug")
        self.startGame = self.cont.actuators['StartGame']
        self.startGame.scene="Game"
        self.mouse = self.cont.sensors['Mouse']
        self.log.msg('init completed')
        
    def update(self):
        
        if self.mouse.positive:
            self.cont.activate(self.startGame)
    
def main():
    cont = bge.logic.getCurrentController()
    own = cont.owner
    
    if 'matrix.menu' not in own:
        own['matrix.menu'] = Menu(cont)
    else:
        own['matrix.menu'].update()

if bge.logic.getCurrentController().mode == 0:
    main() 
import bge 

from Logging import Logging
from mathutils import Vector
'''
Important
===========================================================
Must have an Always Sensor (,,,) to fire off the __init__

'''
class GunControl(object):
    def __init__(self,cont):
        self.log = Logging("GunControl","Debug")
        self.cont = cont
        self.own = cont.owner
        self.scene = bge.logic.getCurrentScene()
        self.bullets = self.own["Bullets"] if self.own["Bullets"] else 0
        self.magazines = self.own["Magazines"] if self.own["Magazines"] else 0
        self.reload = self.cont.sensors["Reload"]
        self.shoot = self.cont.sensors["Shoot"]
        self.aim = self.cont.sensors["Ray"]
        self.gun = self.own.parent
        self.log.msg("Init Completed.")
        
    def update(self):
        if self.aim.positive:
            #Add the laser targeting pointer to the scene
            bge.render.drawLine(self.own.worldPosition,self.aim.hitPosition,[255,0,0])  
            
        if self.reload.positive and self.magazines > 0:
            self._reload() 
            self.gun.state = 1 #flip the gun back to shoot mode
            
        if self.bullets > 0:    
            if self.shoot.positive:
                self._shoot()
        else:
            self.gun.state = 2 #gun is empty
                             
        self._updateHUD()
    
    def _shoot(self):
        self.bullets += -1
        if self.aim.positive:            
            bulletForce = self.scene.addObject("BulletForce",self.own,3)  
            bulletForce.worldPosition = Vector(self.aim.hitPosition) +(Vector(self.aim.hitNormal)*0.01) 
            bulletHole = self.scene.addObject("BulletHole",self.own,200)       
            #position the bullet based on the ray, give a margin factor due to rendering collision
            bulletHole.worldPosition = Vector(self.aim.hitPosition) +(Vector(self.aim.hitNormal)*0.01)
            bulletHole.alignAxisToVect(self.aim.hitNormal,2)
        self._activate(self.cont.actuators["Fire"])
        self._activate(self.cont.actuators["MuzzleFlash"])

    
    def _reload(self):
        #self._activate(self.cont.actuators["Reload"])
        self.magazines += -1
        self.bullets = self.own["Bullets"] if self.own["Bullets"] else 0
    
    def _updateHUD(self):
        bge.logic.sendMessage("Ammo", str(self.bullets)) 
        bge.logic.sendMessage("Clips", str(self.magazines)) 
    
    def _activate(self,actuator):
        self.cont.activate(actuator)

def main():
    cont = bge.logic.getCurrentController()
    own = cont.owner
     
    if 'matrix.gunControl' not in own:
        own['matrix.gunControl'] = GunControl(cont)
    else:
        own['matrix.gunControl'].update()
 
if bge.logic.getCurrentController().mode == 0:
    main() 
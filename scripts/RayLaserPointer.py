from bge import render,logic
from mathutils import Vector

def main(cont):
    own = cont.owner
    scene = logic.getCurrentScene()
    ray = cont.sensors["Ray"]
    #detector = cont.sensors["Detector"]
    reload = cont.sensors["Reload"]
    
    if reload.positive and own["Magazines"] > 0:
        own["Magazines"] += -1
        logic.sendMessage("Clips", str(own["Magazines"]))
        own["Bullets"] = 100
        logic.sendMessage("Ammo", "100") 
        cont.activate(cont.actuators["Reload"])
        
        
    if cont.sensors["Shoot"].positive:

        if own["Bullets"]>0:
            own["Bullets"] += -1
            logic.sendMessage("Ammo", str(own["Bullets"]))
            if ray.positive:
                #Add the laser targeting pointer to the scene
                own["Dist"] = own.getDistanceTo(ray.hitObject)
                render.drawLine(own.worldPosition,ray.hitPosition,[100,255,0])              
                hitObject = ray.hitObject
                bulletForce= scene.addObject("BulletForce",own,3)  
                bulletForce.worldPosition = Vector(ray.hitPosition) +(Vector(ray.hitNormal)*0.01) 
                #bulletForce.worldPosition = cont.ray.worldPosition
                bulletHole= scene.addObject("BulletHole",own,200)       
                #position the bullet baed on the ray, give a margin factor due to rendering collision
                bulletHole.worldPosition = Vector(ray.hitPosition) +(Vector(ray.hitNormal)*0.01)
                bulletHole.alignAxisToVect(ray.hitNormal,2)

            cont.activate(cont.actuators["Fire"])
            #cont.activate(cont.actuators["MuzzleFlash"])
from bge import render,logic
from mathutils import Vector

def main(cont):
    own = cont.owner
    scene = logic.getCurrentScene()
    ray = cont.sensors["Ray"]
    if ray.positive:
        #Add the laser targeting pointer to the scene
        render.drawLine(own.worldPosition,ray.hitPosition,[100,255,0])
        if cont.sensors["Shoot"].positive:
            hitObject = ray.hitObject
            bulletForce= scene.addObject("BulletForce",own,30)  
            bulletForce.worldPosition = Vector(ray.hitPosition) +(Vector(ray.hitNormal)*0.10) 
            bulletHole= scene.addObject("BulletHole",own,200)       
            #position the bullet baed on the ray, give a margin factor due to rendering collision
            bulletHole.worldPosition = Vector(ray.hitPosition) +(Vector(ray.hitNormal)*0.01)
            bulletHole.alignAxisToVect(ray.hitNormal,2)
from bge import logic

def _getForceMagnitude(distance,force,range):
    return (distance*(-force/range))+force

def explode():
    FORCE = 1000
    RANGE = 25
    scene logic.getCurrentScene()
    cont = logic.getCurrentController()
    bomb = cont.owner
    
    for obj in scene.objects:
        if obj.mass:
            vec = obj.worldPosition - bomb.worldPosition
            if vec.magnitude <= RANGE:
                hitObj,_,_ = bomb.rayCast(bomb.worldPosition+vec,bomb.worldPosition)
                if hitObj == obj:
                    vec.magnitude = _getForceMagnitude(vec.magnitude,FORCE,RANGE)
                    obj.applyForce(vec)
    bomb.endObject()

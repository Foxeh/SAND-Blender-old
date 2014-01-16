'''

'''
from bge import logic
DEBUG_MESSAGES = True  
class HitCount(object):
    def __init__(self,cont):
        self.cont = cont
        self.own = cont.owner
        self.hitCount = 0
        self.mutate()
        
    def mutate(self):
        pass
    def update(self):
        self.hitCount +=1
        self.cont.activate(self.cont.actuators["Hit"])
        if (0)<self.hitCount<(3):
            self.cont.activate(self.cont.actuators["Malfunction"])
        else :
            self.cont.activate(self.cont.actuators["Danger"])
        if self.hitCount > self.own["MaxDamage"]:
            bge.logic.sendMessage("Enemy", "-1") 
            self.own.endObject()
	
def main():
	cont = logic.getCurrentController()
	own = cont.owner
	
	if 'my.hitCount' not in own:
		own['my.hitCount'] = HitCount(cont)
	else:
		own['my.hitCount'].update()
	
if logic.getCurrentController().mode == 0:
	main()   
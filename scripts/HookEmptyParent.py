'''
This is a test script for testing out ideas
'''
import bge,mathutils
    
class HookEmpty(object):
    def __init__(self,cont):
        self.cont = cont
        self.own = cont.owner
        self.mutate()
        
    def mutate(self):
        for child in self.own.groupMembers:
            child.setParent(self.own,False,False)
    def update(self):
        print("update")
        #velo = mathutils.Vector((0.0, 0.2, 0.0))
        #self.own.localLinearVelocity = velo
        #for child in self.own.groupMembers:
        #    child.localLinearVelocity = velo
        steering = self.cont.actuators["Steering"]
        self.cont.activate(steering)
 
def isCont(object):
	if str(object.__class__) == "<class 'SCA_PythonController'>":
		return True
	return False

def msg(*args):
	message = ""
	for i in args:
		message += str(i)
		
	if DEBUG_MESSAGES:
		print('[DEBUG] ' + message)
	
#################################

# Module Execution entry point
def main():
	cont = bge.logic.getCurrentController()
	own = cont.owner
	
	if 'my.hookEmpty' not in own:
		own['my.hookEmpty'] = HookEmpty(cont)
	else:
		own['my.hookEmpty'].update()
	
# Non-Module Execution entry point (Script)
if bge.logic.getCurrentController().mode == 0:
	main()   
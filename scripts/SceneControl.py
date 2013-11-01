'''
This is the main scene controller

It is meant to handle all scene level control

This should be parented to an empty in the scene and hooked to an always logic
brick set to True Level Triggering so the scene control update method fires.

'''
import bge
    
class SceneControl(object):
    def __init__(self,cont):
        self.cont = cont
        self.own = cont.owner
        
    def update(self):
        pass
 
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
	
def main():
	cont = bge.logic.getCurrentController()
	own = cont.owner
	
	if 'my.sceneControl' not in own:
		own['my.sceneControl'] = HookEmpty(cont)
	else:
		own['my.sceneControl'].update()
	
if bge.logic.getCurrentController().mode == 0:
	main() 
'''
Finder.py
=========

Allows to find objects within active scenes.
Several matchers allow to search with multiple criterias.

Custom Matchers
---------------
You can define own matchers. 
Matchers are functions that 
- receive the object reference as first parameter
- any number of matching parameters
- return True if the object reference matches the parameters
'''

import GameLogic
__version__ = "1.00" 
__author__ = "Monster"
__date__ = "2011-Dec-07"


def findObjects(matcher, params, scene=None, attribute=None):
	if scene is None:
		objects = []
		for scene in GameLogic.getSceneList():
			objects.extend(findObjects(matcher, params, scene, attribute))
		return objects
	objectsToMatch = retrieveSceneObjects(scene, attribute)
	return [obj for obj in objectsToMatch if matcher(obj, *params)]

#--- Matchers	
def byName(obj, objectName):
	return obj.name == objectName

def byNameContains(obj, partialName):
	return obj.name.find(partialName)>=0

def byProperty(obj, propertyName):
	return propertyName in obj

def byPropertyValue(obj, propertyName, propertyValue):
	try:
		return obj[propertyName] == propertyValue
	except KeyError:
		return False
	
#--- Internal	
def retrieveSceneObjects(scene, attribute):
	if attribute is None:
		attribute = "objects"
	if hasattr(scene, attribute):
		return getattr(scene, attribute)
	 
	scene = findSceneByName(str(scene))
	return getattr(scene, attribute)
		
def findSceneByName(sceneName):	
	if sceneName == "":
		return GameLogic.getCurrentScene()
	
	for scene in GameLogic.getSceneList(): 
		if scene.name == sceneName:
			return scene
		
	raise LookupError(("No active scene with name '%s' found" 
			%  (sceneName)))



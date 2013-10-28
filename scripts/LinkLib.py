""" 
LinkLib.py

It is open source

The LinkLib library contains function to interact between linked groups and
it's pivot objects. 

history:
1.13 	- replaced cache wich instance.
		  instance can be applied to all instance objects
		- addObjTreeToInstance() applies all parented objects
		  to the instance of this object.	
		- setInstanceProperty() distributes the properties
		  of the connected PropertySensors to all instance objects
		  of this instance. This simulates "instance properties".
1.12 	- parenting makes the child no ghost now 
		- added copyPropertyToPivot
1.11	- added cascading property assignment 
				(properties from pivot's pivot)
		- API change! 
			only properties that are defined at the base are copied!
1.10	- removed "baseName" property
		- introduced LinkLibCache
1.8		- compatible with 2.5
1.7		- bugfix: parented pivots might get different position
			then the parent is rotated
1.6 	- enhanced parentPivotsChildrenToOwner to look for children 
			with specific properties listed in property "mustHave". 
1.5 	- added getPivotInTree, parentPivotsChildrenToOwner
		- renamed parentPivot to parentPivotToOwner
1.4 	- added parentPivot, printLinks, printPivotForObj, printBaseForObj, printAll, copyPropsToBase, copyPropsFromPivot
		- BugFix copyProps does not copy the property Pivot, or baseType anymore
1.3 	- added copyPropsAnd, copyPropsOr
1.2 	- refactored the variables for property names, 
		- replaced has_key with in
"""
__version__ = "1.12" 
__author__ = "Monster"
__date__ = "2011-Oct-13"

#property names
PBaseType = "baseType"	# property to identify pivots for a specific link group
PBaseName = "baseName"	# property of the pivot with the name of the base object 
						# base object (without preceeding "OB")
PBase	= "base"		# when successful the pivot will have 
						# this property containing a reference to the base
PPivot 	= "pivot"		# when successful the base will have
						# this property containing a reference to the pivot
PUpdate	= "update"		# update prop to trigger the base to care for new properties
PDebug	= "debug"		# Debug on/off
PMustHave = "mustHave"	# A list of properties that an object must have to be identified

Pinstance = "_instance"
import GameLogic #@UnresolvedImport
import collections

#----BGE module functions
#===============================================================================
# setInstanceProperty
#===============================================================================
def setInstanceProperty(cont):	
	"""
	Distributes the property values to all instance objects 
	of this instance: 
		- if they already have this property
		- if the sensor is positive
	"""
	obj = cont.owner
	instance = getInstance(obj)
	for sensor in cont.sensors:
		if not sensor.positive:
			continue
		instance.setProperty(sensor.propName, obj[sensor.propName])
#===============================================================================
# addObjTreeToInstance
#===============================================================================
def addObjTreeToInstance(cont):	
	"""
	Parents the base to the parent of the pivot.
	Input:
	base
		"debug" property if NOT 0 switches on debug mode
	"""
	own = cont.owner
	instance = getInstance(own)
			
	addTreeToInstance(instance, own)
#===============================================================================
# reparent
#===============================================================================
def reparent(cont):	
	"""
Parents the base to the parent of the pivot.
Input:
	base
		"debug" property if NOT 0 switches on debug mode
		"pivot" property containing a reference to the pivot object
	"""
	
	base = cont.owner
	
	pivot = base.get(PPivot)
	if not pivot:
		print ("reparent() - Error: $s has no pivot attached" % (base.name))
		return

	base.setParent(pivot.parent, False, False)
	if pivot.get(PDebug,0) >= 50: print ("%s with %s reparented to %s" % (base.name, pivot.name, base.parent.name))		

#===============================================================================
# parent
#===============================================================================
def parent(cont):	
	"""
Parents the base to the pivot.
Input:
	base
		"debug" property if NOT 0 switches on debug mode
		"pivot" property containing a reference to the pivot object
"""
	
	base = cont.owner
	
	pivot = base.get(PPivot)
	if not pivot:
		print ("parent() - Error: %s has no pivot attached" % (base.name))
		return

	base.setParent(pivot, False, False)
	if pivot.get(PDebug,0) >= 50: print ("%s with %s parented to %s" %(base.name, pivot.name, base.parent.name))

#===============================================================================
# copyProps
#===============================================================================
def copyProps(cont):
	copyPropsToBase(cont)
	
#===============================================================================
# copyPropsToBase
#===============================================================================
def copyPropsToBase(cont):
	"""
Copies the existing properties from this pivot object to 
the base object. 
Requires a set base
"""
	pivot = cont.owner
	
	base = pivot.get(PBase)
	if not base:
		print ("copyPropsToBase() - Error: %s has no base attached" % (pivot.name))
		return
		
	copyProperties( pivot, base )
	base[PUpdate]=True
	
#===============================================================================
# copyPropsFromPivot
#===============================================================================
def copyPropsFromPivot(cont):
	"""
Copies the existing properties from the pivot object to 
the this base object. 
Requires a set pivot.
"""
	base = cont.owner
	
	pivot = base.get(PPivot)
	if not pivot:
		print ("copyPropsFromBase() - Error: %s has no pivot attached" % (base.name))
		return
		
	copyProperties( pivot, base )
	base[PUpdate]=True

#===============================================================================
# copyPropsAnd
#===============================================================================
def copyPropsAnd(cont):
	"""
Copies the existing properties from the pivot object to 
the base object of the group instance if all sensors are positive 
Requires a set pivot or base
"""
	for sensor in cont.sensors:
		if not sensor.positive:
			return

	copyProps(cont)
		
#===============================================================================
# copyPropsOr
#===============================================================================
def copyPropsOr(cont):
	"""
Copies the existing properties from the pivot object to 
the base object of the group instance if at least one sensor is positive 
Requires a set pivot or base
"""
	for sensor in cont.sensors:
		if sensor.positive:
			break
	else:
		return
	
	copyProps(cont)

#===============================================================================
# copyPropertyToPivot
#===============================================================================
def copyPropertyToPivot(cont):
	''' 
	Copies the property from the property sensor to the parent.
	Deals with multiple sensors. Only properties configured in 
	the sensors are copied and only for positive sensors.
	'''
	
	base = cont.owner
	pivot = getPivot(base)
	
	source = base
	target = pivot
	
	for sensor in cont.sensors:
		if not sensor.positive:
			continue
		
		try:
			propertyName = sensor.propName
		except AttributeError:
			continue

		value = source[propertyName]
		try:
			if target[propertyName] == value:
				continue
		except KeyError:
			continue
		target[propertyName] = value
		
#===============================================================================
# linkPivotAndBase
#===============================================================================
def linkPivotAndBase(cont):
	linkObjectToPivot(cont.owner)
#===============================================================================
# linkSceneObjects
#===============================================================================
def linkSceneObjects(cont):
	linkObjects(GameLogic.getCurrentScene().objects)
	
#===============================================================================
# parentPivotToOwner
#===============================================================================
def parentPivotToOwner(cont):
	pivot = getPivotInTree(cont)	
	if pivot== None:
		return
	if pivot.get(PDebug,0) >= 50:print ("parent %s->%s" %(pivot.name,cont.owner.name))
	pivot.setParent( cont.owner, False, False )
	
#===============================================================================
# parentPivotsChildrenToOwner
#===============================================================================
def parentPivotsChildrenToOwner(cont):
	'''
	Parents the children of the pivot to the owner of this controller.
	Requires the Base object.
	If the property mustHave is set only children with a property listed
	in mustHave's value are parented. Very useful to parent objects to 
	various group objects.
	@param cont:
	'''
	pivot = getPivotInTree(cont)
	if pivot== None:
		return
	own = cont.owner
	mustHave = own.get(PMustHave)
	if mustHave != None:
		mustHaves = mustHave.split()

	for child in pivot.children:
		if isParentOf(child,own):
			continue
		
		if mustHave!=None:
			if not isOnePropInObject(mustHaves, child):
				continue
			
		if pivot.get(PDebug,0) >= 75:print ("ppcto - from %s reparent %s->%s" %(child.parent.name, child.name, own.name))
		child.removeParent()
		child.setParent(own, False, False)

#===============================================================================
# assignPivotFromParent
#===============================================================================
def assignPivotFromParent(cont):
	own = cont.owner
	obj = own
	pivot = None
	while (obj is not None and 
			pivot is None):
		pivot = obj.get(PPivot)
		obj = obj.parent
	
	if pivot is None:
		return
	
	own[PPivot] = pivot	
#---- print functions 
#===============================================================================
# printLinks
#===============================================================================
def printLinks(cont):
	if not cont.sensors[0].positive:
		return
	printPivotForObj(cont.owner)
	printBaseForObj(cont.owner)
	
#===============================================================================
# printAll
#===============================================================================
def printAll(cont):
	if not cont.sensors[0].positive:
		return
	
	for obj in GameLogic.getCurrentScene().objects:
		if PBase in obj:
			printBaseForObj(obj)
			
#--- Internals
#===============================================================================
# addTreeToInstance
#===============================================================================
def	addTreeToInstance(instance, obj):
	while obj.parent is not None:
		obj = obj.parent
		
	addChildrenToInstance(instance, obj)
#===============================================================================
# addChildrenToInstance
#===============================================================================
def addChildrenToInstance(instance, obj):
	if obj is None:
		return
	
	instance.addInstanceObject(obj)
	for child in obj.children:
		addChildrenToInstance(instance, child)
#===============================================================================
# linkObjectToPivot
#===============================================================================
def linkObjectToPivot(base):		
	"""
Parents the base object of a group instance to the pivot object 
and vice versa.
Important: 
	!!! Run this method in priority mode !!!
Input:
	pivot 
		"baseName" string property with the name of the base (without "OB")
		or
		has a property with the name of the base property 
	base
		"baseType" contains the name of the property for pivot objects
		"debug" property if NOT 0 switches on debug mode
Output:
	The pivot will get a property "base" referencing the base object 
	The base will get a property "pivot" referencing the pivot object 
"""
	#==============================================================================
	# roundString
	#==============================================================================
	def roundString(obj, places=7):
		try:
			for item in obj:
				break
		except TypeError:
			# not iterable assume single value
			result =  str(round(float(obj), places))
			if result == "-0.0":
				return "0.0"
			return result
		
		#it is iterable
		result = "["
		for item in obj:
			if result != "[":
				result += ", "
			result += roundString(item, places)
		result += "]"
		return result

	#==============================================================================
	# identifyPivot
	#==============================================================================
	def identifyPivot(base):
		"""
	Looks for a pivot that meets following criteria relative to base:
		same position
		same orientation
		has NO property "base"
		has property "baseName" with the name of the base
		is NOT base
	Input:
		base
			"baseName" property containing the name of the base object (without "OB")
	"""	
		#=============================================================================
		# nearlyEqual
		#=============================================================================
		def nearlyEqual(objectA, objectB):
			return ( roundString(objectA)==roundString(objectB) )
		
		# I would prefer to read the group name directly but it is not available.
		# Therefore the group name should be in property baseType
		#==============================================================================
		baseType = base[PBaseType]
		for obj in GameLogic.getCurrentScene().objects:
			if (baseType in obj and
				obj is not base and
				PBase not in obj and
				nearlyEqual(obj.worldPosition, base.worldPosition) and
				nearlyEqual(obj.worldOrientation, base.worldOrientation) ):
				return obj
	
		print ("%s- no pivot found with %s" %(base.name, baseType))
		return None
	#==============================================================================
	pivot = base.get(PPivot)
	if pivot:
		if pivot.get(PDebug,0) >= 30: print ("%s already assigned to %s" % (base.name, pivot.name))
		return
	
	if not PBaseType in base:
		print ("linkObjectToPivot() - Error: %s is not a base - missing property %s" %(base.name, PBaseType))
		return

	pivot = identifyPivot(base)
	if not pivot:
		print ("linkObjectToPivot() - Error: %s no pivot identified" %(base.name))
		return
	
	# store references to both directions
	pivot[PBase] = base
	base[PPivot] = pivot
	
	Instance(base,pivot)
	if pivot.get(PDebug,0) >= 50:	print ("linkObjectToPivot() - %s base: %s pivot: %s" % (base[PBaseType], base.name, pivot.name))
#==============================================================================
# copyProperties
#==============================================================================
def copyProperties( pivot, base ):
	baseType = base[PBaseType]
	for propName in base.getPropertyNames():
		# do not copy linkLib specific properties
		if  ( not propName.startswith("_")
		and propName!=PBase 
		and propName!=PPivot 
		and propName!=baseType 
		and propName!=PBaseType 
		and propName!=PBaseName
		and propName in pivot):
			base[propName]=pivot[propName]
			if pivot.get(PDebug,0) >= 75: print ("%s [%s] =%s [%s]==%s" % (base.name, propName, pivot.name, propName, base[propName]))

	pivotsPivot = getPivot(pivot)
	if pivotsPivot is None:
		return
	
	# cascading links
	copyProperties(pivotsPivot, base)
	
#===============================================================================
# linkObjects
#===============================================================================
def linkObjects(objects):
	for object in objects:
		if PBaseType in object:
			linkObjectToPivot(object)

#===============================================================================
# getPivotInTree
#===============================================================================
def getPivotInTree(cont):
	pivot = getPivotInParents(cont.owner)
	if pivot is not None:
		return pivot
	
	for sensor in cont.sensors:
		if PPivot in sensor.owner:
			pivot = sensor.owner[PPivot]
			return pivot
	print ("warning no pivot for %s found" % (cont.owner.name))
	
#===============================================================================
# getPivotInTree
#===============================================================================
def getPivotInParents(own):
	pivot = None
	obj = own
	while (obj is not None and pivot is None):
		pivot = own.get(PPivot)
		obj = obj.parent
		
	if pivot is None:
		return
	return pivot
			
#===============================================================================
# printPivotForObj
#===============================================================================
def printPivotForObj(own):
	pivot = own.get(PPivot)
	if pivot: print ("p %s base: %s pivot: %s" %(own[PBaseType], own.name, pivot.name))
	
#===============================================================================
# printBaseForObj
#===============================================================================
def printBaseForObj(own):
	base = own.get(PBase)
	if base:  print ("b %s base: %s pivot:" %(base[PBaseType], base, own))

#===============================================================================
# isOnePropInObject
#===============================================================================
def isOnePropInObject(propertyNames, object):
	for propertyName in propertyNames:
		if propertyName in object:
			return True
		
#===============================================================================
# isParentOf
#===============================================================================
def isParentOf(obj, child):
	parent = child
	while parent!=None:
		if parent == obj:
			return True
		parent = parent.parent

#===============================================================================
# printParents
#===============================================================================
def getParentString(child):
	parent = child
	result = ""
	while parent!=None:
		result += parent.name+"->"
		parent = parent.parent
	return result

#===============================================================================
# getInstance
#===============================================================================
def getInstance(obj):
	instance = obj.get(Pinstance)
	if not isinstance(instance, Instance):
		return None
	return instance

#===============================================================================
# getPivot
#===============================================================================
def getPivot(obj):
	instance = getInstance(obj)
	if instance is None:
		return None
	return instance.pivot

#===============================================================================
# getBase
#===============================================================================
def getBase(obj):
	instance = getInstance(obj)
	if instance is None:
		return None
	return instance.base

#--- Classes
#===============================================================================
# Instance
#===============================================================================
class Instance(object):
	def __init__(self, base, pivot):
		self.instanceObjects = []

		self.base = base
		self.pivot = pivot 

		self.addInstanceObject(base)
		self.addInstanceObject(pivot)
		
	def addInstanceObject(self, gameObject):
		if gameObject in self.instanceObjects:
			return
		
		self.instanceObjects.append(gameObject)
		gameObject[Pinstance] = self
		
	def setProperty(self, propertyName, value, force=False):
		for instanceObject in self.instanceObjects:
			if (not force and 
			    propertyName not in instanceObject):
				continue
			instanceObject[propertyName] = value
		
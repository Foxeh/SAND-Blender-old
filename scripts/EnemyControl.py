"""
This script is to control the spawn point and the destination point 
"""
import finder
import bge #Import game engine functions
from Logging import Logging

log = Logging("EnemyControl","Debug")

enemy = finder.findObjects(finder.byNameContains, ["GroupMo_proxy"], None, "objectsInactive")[0]
#navmesh = finder.findObjects(finder.byNameContains, ["NavMesh1"], "")[0]
#print(dir(navmesh))
cont = bge.logic.getCurrentController() #Get the controller the script is attached to
own = cont.owner #Get the object running the code. Unused in this script but good to know

enemyActuator = cont.actuators['EnemyActuator']
enemyActuator.object = enemy

move_data = None
message_sensor = cont.sensors["SpawnEnemyMessage"]

#IMPORTANT the message sensor sends 2 pulses in a row
# need to check that the sensor is positive then act
if message_sensor.positive :   
    move_data = message_sensor.bodies[message_sensor.subjects.index("SpawnEnemy")]
    moveProps = move_data.split(',')
    srcIP = own['srcIP']
    if moveProps[0].endswith(srcIP):       
        print("message sensor:",moveProps[0])
        target = finder.findObjects(finder.byNameContains, [moveProps[1]], "")[0]
        enemyMotion = enemy.actuators["Steering"]
        enemyMotion.target = target  
        #enemyMotion.navmesh = navmesh  
        cont.activate(enemyActuator)
        bge.logic.sendMessage("Enemy", "1") 
    else:
        print("bad")
from bge  import logic, render
from Logging import Logging

class GunHID(object):
    gun = {'key1':1,
            'key2':2,
            'key3':4,
            'key4':8,
            'key5':16,
            'key7':32,
            'key8':64,
            'key8':128,
            'key9':256,
            'key10':512,
            'hatCenter':1,
            'hatLeft':2,
            'hatRight':4,
            'hatForward':8,
            'hatBack':16
            }
    
    def __init__(self,mousemovecore):   
        self.core = mousemovecore    
        self.cont = self.core.cont
        self.log = Logging("GunHID","Debug")
        self.log.msg("Init Completed.")
        
    def getWindowSize(self):
        return (render.getWindowWidth(), render.getWindowHeight())    
       
    def getCenter(self):
        size = self.getWindowSize()
        screenCenter = (size[0]//2, size[1]//2)
        
        return (screenCenter[0] * (1.0/size[0]), screenCenter[1] * (1.0/size[1]))
    
    def layout(self,controls): 
        
        if(self.recieveGunMsg()):  
            

            
            controls.forward = 2 if (self.hat&self.gun['hatForward']==self.gun['hatForward']) else 0       
            controls.back = 2 if (self.hat&self.gun['hatBack']==self.gun['hatBack']) else 0
            controls.left = 2 if (self.hat&self.gun['hatLeft']==self.gun['hatLeft']) else 0
            controls.right = 2 if (self.hat&self.gun['hatRight']==self.gun['hatRight']) else 0   
            
                     
            controls.up = 0
            controls.down = 0            
            controls.crouch = 0
            controls.run = 0
        else:
            controls.forward = 0      
            controls.back = 0
            controls.left = 0
            controls.right = 0           
            controls.up = 0
            controls.down = 0            
            controls.crouch = 0
            controls.run = 0
        
    def recieveGunMsg(self):
        gunpos = self.cont.sensors["GunPos"]
        if(gunpos.positive):
            gunData = [ i for i in gunpos.bodies[gunpos.subjects.index("GunPos")].split(',')]
            
            self.pitch = self.convert(float(gunData[0])*-1)
            self.roll = self.convert(float(gunData[1])*-1)
            
            self.trigger = int(float(gunData[2]))
            self.wheel = int(float(gunData[3]))
            self.hat = int(float(gunData[4]))
            self.keys = int(float(gunData[5]))
            
            if(self.trigger):
                self.log.msg("trigger")
                logic.sendMessage("Trigger", '1') 
            
            #self.log.msg("hat: "+str(self.hat)) 
            return True
        
    def convert(self,x):
        return (x+5)/10
            
    def pos(self):
        if(self.recieveGunMsg()):           
            return [self.roll,self.pitch]           
        else:
            return logic.mouse.position

    
    
    
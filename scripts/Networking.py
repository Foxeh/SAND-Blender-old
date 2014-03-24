"""
Game networking class to handle UDP comms from server
"""

import socket
import struct
from Logging import Logging
from Messages import Messages,Message

class ProtocolHandler(object):
    '''
    Struct-based Binary Protocol Definition (UDP)
    =============================================
        < = little endian
        L = Source IP (integer)
        L = Destination IP (integer)
    '''
    def __init__(self):
        self.protocolFormat = '<LL'
        self.log = Logging("ProtocolHandler","Debug")
        self.log.msg("Init Completed.")
        
    def parse(self,rawData):
        data = struct.unpack(self.protocolFormat,rawData)
          
        payload = {}
        payload['source'] = self._dec2dot(data[0])
        payload['dest'] = self._dec2dot(data[1])
        #TODO: define the rest of the network data protocol here.....
        
        msg = Message("networkdata",payload)
        
        return msg
            
    def _dec2dot(self,numbericIP):
        if type(numbericIP) == types.StringType and not numbericIP.isdigit() :
            return None
        numIP = long(numbericIP)
        return "%d.%d.%d.%d" % ((numIP>>24)&0xFF, (numIP>>16)&0xFF, (numIP>>8)&0xFF, numIP&0xFF)
        
class Networking(object):
    def __init__(self,cont=None):
        self.cont = cont
        self.host = "0.0.0.0"
        self.port = 10001
        self.protocol = ProtocolHandler()
        self.socketClient = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.socketClient.bind((self.host, self.port))
        self.socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 256)
        self.socketClient.setblocking(0)
        
        self.messages = Messages(self.cont,self)
        
        self.log = Logging("Networking","Debug")
        self.log.msg("Init Completed.")
        
    def update(self):
        try:      
            rawData, SRIP = self.socketClient.recvfrom(256)
            data = self.protocol.parse(rawData)
            self.log.msg(data)
            #bge.logic.sendMessage("SpawnEnemy", data) 
            self.messages.send(msg)                 
        except :
            pass
        
        
        
        
        

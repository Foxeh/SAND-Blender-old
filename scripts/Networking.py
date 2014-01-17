"""
Game networking class to handle UDP comms from server
"""
import bge #Import game engine functions
import socket
import struct
from Logging import Logging

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
        return str(data[0])+","+str(data[1])
            
    def _dec2dot(numbericIP):
        if type(numbericIP) == types.StringType and not numbericIP.isdigit() :
            return None
        numIP = long(numbericIP)
        return "%d.%d.%d.%d" % ((numIP>>24)&0xFF, (numIP>>16)&0xFF, (numIP>>8)&0xFF, numIP&0xFF)
        
class Networking(object):
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 10001
        self.protocol = ProtocolHandler()
        self.socketClient = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.socketClient.bind((self.host, self.port))
        self.socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 256)
        self.socketClient.setblocking(0)
        self.log = Logging("Networking","Debug")
        self.log.msg("Init Completed.")
        
    def update(self):
        try:      
            rawData, SRIP = self.socketClient.recvfrom(256)
            data = self.protocol.parse(rawData)
            #self.log.msg(data)
            bge.logic.sendMessage("SpawnEnemy", data, "Source", "Source")                  
        except :
            pass
        

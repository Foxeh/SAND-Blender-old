"""
Game networking class to handle UDP comms from server
"""
import bge
import socket
import struct
from Logging import Logging

class GunUdpHandler(object):
    def __init__(self):
        self.protocolFormat = '<ffffff'
        self.log = Logging("GunUDPHandler","Debug")
        self.log.msg("Init Completed.")
        
    def parse(self,rawData):
        try:
            data = struct.unpack(self.protocolFormat,rawData)
            #self.log.msg("data: "+str(data[0])+" "+str(data[1]))
            return str(data[0])+','+str(data[1])+','+str(data[2])+','+str(data[3])+','+str(data[4])+','+str(data[5])
        except Exception as e:
            self.log.msg("error: "+str(e))
        
class GunUdpListener(object):
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 10002
        self.protocol = GunUdpHandler()
        self.socketClient = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.socketClient.bind((self.host, self.port))
        self.socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 256)
        self.socketClient.setblocking(0)
        self.log = Logging("GunUdpListener","Debug")
        self.log.msg("Init Completed.")
        
    def update(self):
        try:      
            rawData, SRIP = self.socketClient.recvfrom(256)
            #self.log.msg(rawData)
            data = self.protocol.parse(rawData)
            #self.log.msg(data)
            bge.logic.sendMessage("GunPos", data)                  
        except Exception as e:
            #self.log.msg(e)
            pass
if __name__ == '__main__':
    s = GunUdpListener()
    while(True):
        s.update()
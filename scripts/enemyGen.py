import socket
import struct
import math, random
import sys, time
import types
'''
This is the enemy generatorp
'''
def dot2dec(ipForm, useHex=False):
    if type(ipForm) == types.StringType:
        ipf = ipForm.split(".")
    elif type(ipForm) in (types.ListType, types.TupleType):
        ipf = ipForm
    elif type(ipForm) in (types.LongType, types.IntType):
        return None
    return reduce(lambda a, b: long(a) * 256 + long(b), ipf)

def dec2dot(numbericIP):
    if type(numbericIP) == types.StringType and not numbericIP.isdigit() :
        return None
    numIP = long(numbericIP)
    return "%d.%d.%d.%d" % ((numIP >> 24) & 0xFF, (numIP >> 16) & 0xFF, (numIP >> 8) & 0xFF, numIP & 0xFF)

# fake addresses
srcnodes = ["192.168.100.120", "192.168.100.121", "192.168.100.122", "192.168.100.123", "192.168.100.124"]
dstnodes = ["192.168.100.124", "192.168.100.123", "192.168.100.120", "192.168.100.122", "192.168.100.121"]

# replace localhost with network name of game machine defined in game blend
HOST, PORT = "localhost", 10001  

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Generate random number of bots
maxBots = random.randint(50, 200)
print("Max # of Bots: " + str(maxBots))

for j in range(1, maxBots):
    for i in srcnodes:
        src = int(dot2dec(srcnodes[random.randint(0, 4)]))
        
        dst = int(dot2dec(dstnodes[random.randint(0, 4)])) 
#        print src, dst
        data = struct.pack('<LL', src, dst)
        # print data
        sock.sendto(data, (HOST, PORT))
        
        # Random time
        genDelay = random.randint(0, 10)
        time.sleep(genDelay)  # estimate Frame rate, might want to use some type of sync btw client and server
        print("Bot Generated")

data = struct.pack('<LL', 0, 0)
sock.sendto(data, (HOST, PORT))

sock.close()
















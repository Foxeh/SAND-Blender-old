import socket
import struct
import math, random
import sys, time
import types
import json
'''
This is reads in the sand-storm analytic result and sends it to the sand-construct
'''
class DataProducer(object):
    def __init__(self): 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def dot2dec(self, ipForm, useHex=False):
        if type(ipForm) == types.StringType:
            ipf = ipForm.split(".")
        elif type(ipForm) in (types.ListType, types.TupleType):
            ipf = ipForm
        elif type(ipForm) in (types.LongType, types.IntType):
            return None
        return reduce(lambda a, b: long(a) * 256 + long(b), ipf)
    
    def dec2dot(self, numbericIP):
        if type(numbericIP) == types.StringType and not numbericIP.isdigit() :
            return None
        numIP = long(numbericIP)
        return "%d.%d.%d.%d" % ((numIP >> 24) & 0xFF, (numIP >> 16) & 0xFF, (numIP >> 8) & 0xFF, numIP & 0xFF)
    
    def main(self):
        HOST, PORT = "192.168.100.146", 10002
        i = 0
        with open("../data/sand-results.json") as f:
            for line in f:
                data = json.loads(line)
                origNetFlow = json.loads(data['json'])

                data = struct.pack('<LLLLLL', self.dot2dec(str(origNetFlow['src_addr'])),self.dot2dec(str(origNetFlow['dst_addr'])),data['src-port'],data['dst-port'],data['flow-time'],data['src-dst-time'])
                self.sock.sendto(data, (HOST, PORT))
                i = i+1
                print(i)
                genDelay = random.randint(0, 2)
                time.sleep(0.1)
        print("sent %i"%i)
        self.sock.close()

if __name__ == '__main__':
    o = DataProducer()
    o.main()
















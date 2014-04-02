from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer
import socket
import struct
import math, random
import sys, time
import types
import json
#TODO: might want to make this a daemon at some point
class KafkaConsumer(object):
    def __init__(self):
        self.myKafka = KafkaClient("192.168.240.195", 9092)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def dot2dec(self, ipForm, useHex=False):
        if type(ipForm) == types.StringType:
            ipf = ipForm.split(".")
        elif type(ipForm) in (types.ListType, types.TupleType):
            ipf = ipForm
        elif type(ipForm) in (types.LongType, types.IntType):
            return None
        return reduce(lambda a, b: long(a) * 256 + long(b), ipf)
    
    def parse(self,obj):
        #TODO: make this a little cleaner
        data = obj.json        
        return struct.pack('<LLLLLL', self.dot2dec(str(data['src_addr'])),self.dot2dec(str(data['dst_addr'])),obj['src-port']['prediction'],obj['dst-port']['prediction'],obj['flow-time']['prediction'],obj['src-dst-time']['prediction'])        
    
    def main(self):
        HOST, PORT = "192.168.240.185", 10002
        try:
            while True:
                #TODO:do we need to add a group name to the consumer???
                consumer = SimpleConsumer(self.myKafka, "", "sand-results")
                for message in consumer:
                    data = json.loads(message)
                    print (data)
                    payload = self.parse(data)
                    self.sock.sendto(payload, (HOST, PORT))
                
        except KeyboardInterrupt:
            print "CTRL-C pressed"
            
        self.myKafka.close()
        self.sock.close()

if __name__ == '__main__':
    o = KafkaConsumer()
    o.main()
    
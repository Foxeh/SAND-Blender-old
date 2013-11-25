DEBUG_MESSAGES = True
class Logging(object):
    def __init__(self,source,level):
        self.level = level
        self.source = source
    def msg(self, message):		
        if DEBUG_MESSAGES:
            print ("[%s] - %s - %s"%(self.level,self.source,message))
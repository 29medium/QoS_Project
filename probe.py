import time

class Probe:
    def __init__(self,seq, timestamp=None):
        if isinstance(seq, bytes):
            self.fromBytes(seq)
        else:
            self.seq = seq
            self.timestamp = timestamp

    def toBytes(self):
        return (str(self.seq)+ "|" +str(self.timestamp)).encode('utf-8')
    
    def fromBytes(self,bytes):
        msg = bytes.decode('utf-8').split('|')
        self.seq = int(msg[0])
        self.timestamp = float(msg[1])
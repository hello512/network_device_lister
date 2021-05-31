import sys
import time
import socket
import random

ICMP = socket.getprotobyname("icmp")

SOCK = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP)

host = socket.gethostbyname(socket.gethostname())


class ICMPHeader:
    def __init__(self, typ=8, code=0, checksum=False):
        self.type = typ
        self.code = code
        self.checksum = self.calc_checksum() if not checksum else checksum


    def calc_checksum(self):
        #this function is wrong :D
#        block = (self.type << 8)|self.code
        return 1236#~block

    def get_bytes(self):
        print(self.checksum & 0xffffffff)
        return self.type.to_bytes(1, "big") + self.code.to_bytes(1, "big") + self.checksum.to_bytes(2, "big")

class ICMPMessage:
    def __init__(self, header):
        self.header = header.get_bytes()
        self.timestamp = int(time.time())
        self.identifier = random.randint(0, 2**15 - 1)
        self.sequence_num = random.randint(0, 2**15 - 1)
        self.data = b"hello world"

    def getbmessage(self):
        print(self.timestamp)
        return self.header + self.identifier.to_bytes(2, "big") + self.sequence_num.to_bytes(2, "big") + self.timestamp.to_bytes(4, "big") + int(0).to_bytes(4, "big") + self.data

def ping():
    pass

#sendto recvfrom

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ip = sys.argv[1]
    else:
        print("no ip was specified")
    print(ip)
    print("socket closed")
    print(socket.gethostbyname(socket.gethostname()))

    header = ICMPHeader()
    message = ICMPMessage(header)

    host = socket.gethostbyname(socket.gethostname())
    print("host: ", host)
    SOCK.bind(("192.168.0.218", 0))

    #message = b"hello world"


    target = "192.168.0.1"

    SOCK.sendto(message.getbmessage(), (target, 1))

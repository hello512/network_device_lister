import sys
import time
import socket
import random

ICMP = socket.getprotobyname("icmp")

SOCK = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP)

host = socket.gethostbyname(socket.gethostname())


class ICMPHeader:
    def __init__(self, typ=8, code=0, checksum=0):
        self.type = typ
        self.code = code
        self.checksum = checksum

    def get_bytes(self):
        print(self.checksum & 0xffffffff)
        return self.type.to_bytes(1, "big") + self.code.to_bytes(1, "big") + self.checksum.to_bytes(2, "big")

class ICMPMessage:
    def __init__(self, header=ICMPHeader()):
        self.header = header #header always consists of 4 bytes
        self.timestamp = int(time.time())
        self.identifier = random.randint(0, 2**15 - 1)
        self.sequence_num = random.randint(0, 2**15 - 1)
        self.data = b"hello worl"

        self.calc_checksum() #needs to be changed

    def calc_checksum(self):
        bytestr = self.getbmessage()
        bytelist = [ord(bytestr[i * 2: i * 2 + 2]) for i in range(len(bytestr) // 2)] ##not acounting for the fact that self.data could not be a multiple of two
        print(bytelist)
        s = sum(bytelist)
        print(s)

        s = (s >> 16) + (s >> s & 0xffff)
        s += (s >> 16)


        #block = (self.type << 8)|self.code
        self.header.checksum = ~s & 0xffff

    def getbmessage(self):
        print(self.timestamp)
        return self.header.get_bytes() + self.identifier.to_bytes(2, "big") + self.sequence_num.to_bytes(2, "big") + self.timestamp.to_bytes(4, "big") + int(0).to_bytes(4, "big") + self.data

def ping():
    pass

#sendto recvfrom
#the checksum is calculated over the whole message

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

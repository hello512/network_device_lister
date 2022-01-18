import sys
import time
import socket
import random

ICMP = socket.getprotobyname("icmp")


class ICMPHeader:
    def __init__(self, typ=8, code=0, checksum=0):
        self.type = typ
        self.code = code
        self.checksum = checksum

    def from_bytes(self, bytes):
        if len(bytes) != 4:
            return False
        self.type = bytes[0]
        self.code = bytes[1]
        self.checksum = int.from_bytes(bytes[2:4], "big")

    def get_bytes(self):
        ####print(self.checksum & 0xffffffff)
        return self.type.to_bytes(1, "big") + self.code.to_bytes(1, "big") + self.checksum.to_bytes(2, "big")

class ICMPMessage:
    def __init__(self, header=ICMPHeader()):
        self.header = header #header always consists of 4 bytes
        self.identifier = random.randint(0, 2**15 - 1)
        self.sequence_num = random.randint(0, 2**15 - 1)
        self.timestamp = int(time.time())
        self.data = b"hello worl"

        self.calc_checksum() #needs to be changed

    def calc_checksum(self):
        ##  calculates checksum
        ##  seems to work
        bytestr = self.getbmessage()
        sum = 0
        bytelist = [bytestr[i * 2: i * 2 + 2] for i in range(len(bytestr) // 2)] ##not acounting for the fact that self.data could not be a multiple of two
        for b in bytelist:
            #####print(bytelist)
            sum += b[0] * 256 + b[1]
            sum = sum & 0xffffffff

        sum = (sum>>16) + (sum & 0xffff)
        sum = sum + (sum>>16)
        self.header.checksum = ~sum & 0xffff

    def check_echo(self, echo):
        if echo.header.code != 0 and echo.header.type != 0:
            return False
        if echo.identifier == self.identifier and echo.sequence_num == self.sequence_num:
            return True
        return False


    def getbmessage(self):
        ##print(self.timestamp)
        return self.header.get_bytes() + self.identifier.to_bytes(2, "big") + self.sequence_num.to_bytes(2, "big") + self.timestamp.to_bytes(4, "big") + int(0).to_bytes(4, "big") + self.data


class ICMPConnection:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP)
        #self.sock.bind(("192.168.0.218", 0)) # really need to fix this.
        #self.sock.bind((socket.gethostname(), 0)) # seems to find the right host.

    def send(self, target, message):
        ##print(target, message.getbmessage())
        self.sock.sendto(message.getbmessage(), (target, 1))

    def recv_raw(self, timeout=0):
        self.sock.settimeout(timeout)
        try:
            return self.sock.recvfrom(65565)
        except:
            return False


    def recv(self, timeout=0):
        # returns a ICMPMessage object
        #23
        msg = ICMPMessage()
        bmsg = self.recv_raw(timeout)
        if bmsg == False:
            return False
        bmsg = bmsg[0][20:]
        msg.header.from_bytes(bmsg[0:4])
        msg.identifier = int.from_bytes(bmsg[4:6], "big")
        msg.sequence_num = int.from_bytes(bmsg[6:8], "big")
        ##print(bmsg[10:12])
        if bmsg[12:16] == b"\x00\x00\x00\x00":
            msg.timestamp = int.from_bytes(bmsg[8:12], "big")
            msg.data = bmsg[16:]
        else:
            msg.timestamp = False
            msg.data = bmsg[8:]
        return msg



#sendto recvfrom
#the checksum is calculated over the whole message

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ip = sys.argv[1]
    else:
        print("no ip was specified")
    ##print(ip)
    ##print("socket closed")
    ##print(socket.gethostbyname(socket.gethostname()))

    header = ICMPHeader()
    message = ICMPMessage(header)
    con = ICMPConnection()

    #host = socket.gethostbyname(socket.gethostname())
    ###print("host: ", host)
    #SOCK.bind(("192.168.0.90", 0))

    #message = b"hello world"


    target = "192.168.0.1"

    con.send(target, message)
    #b = con.recv(1)

import sys
import socket

ICMP = socket.getprotobyname("icmp")

SOCK = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP)

host = socket.gethostbyname(socket.gethostname())

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

    host = socket.gethostbyname(socket.gethostname())
    SOCK.bind((host, 0))

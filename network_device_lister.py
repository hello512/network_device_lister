##	this scripts lists all pingable devices in the local network

import sys
import icmp
import time
import socket
import threading


CONNECTIONS = []
MSGS = []

def ping(ip):
	con = icmp.ICMPConnection()
	header = icmp.ICMPHeader()
	msg = icmp.ICMPMessage(header)
	MSGS.append(msg.getbmessage())
	#try:
	con.send(ip, msg)
	rm = con.recv(1)#.getbmessage())
	#print(rm)
	if rm.getbmessage() in MSGS:
		print(ip, "worked")
	#except:
	#	print(ip, "not working")

#for testing purposes: ip range from 0.0 to 0.255
def ping_all():
	t0 = time.time()
	con = icmp.ICMPConnection()
	for i in range(0, 256):
		header = icmp.ICMPHeader()
		msg = icmp.ICMPMessage(header)
		MSGS.append((msg, "192.168.0." + str(i)))
		#try:
		con.send("192.168.0." + str(i), msg)

		#t = threading.Thread(target=ping, args=["192.168.0." + str(i)])
		#t.start()
		#CONNECTIONS.append(t)
	while True:
		rm = con.recv(1)
		for m in MSGS:
			if m[0].check_echo(rm):
				print(m[1], "worked")




if __name__ == "__main__":
	ping_all()
	#print(MSGS)
"""
	con = icmp.ICMPConnection()
	msg = icmp.ICMPMessage()
	print(msg.getbmessage())
	con.send("192.168.0.1", msg)
	rm = con.recv(1)
	print(rm.getbmessage())
"""

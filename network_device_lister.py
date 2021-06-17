##	this scripts lists all pingable devices in the local network

import sys
import icmp
import time
import socket
import threading


CONNECTIONS = []
MSGS = []

#for testing purposes: ip range from 0.0 to 0.255
def ping_all(args):
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
		if not rm:
			print("stoping program: timed out")
			break
		for m in MSGS:
			if m[0].check_echo(rm):
				print(m[1], "	answered in: ", time.time() - rm.timestamp, "	seconds")


class Args:
	def __init__(self, file_name="", start_ip="192.168.0.1", end_ip="192.168.0.255"):
		self.file_name = file_name
		self.start_ip = start_ip
		self.end_ip = end_ip


def analyse_args():
	args = Args
	for i, a in enumerate(sys.argv):
		if a == "-s":
			args.start_ip = sys.argv[i + 1]

		if a == "-e":
			args.end_ip = sys.argv[i + 1]

		if a == "-f":
			args.file_name = sys.argv[i + 1]

		print(a)



if __name__ == "__main__":
	args = analyse_args()
	ping_all(args)

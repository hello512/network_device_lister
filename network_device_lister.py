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

	args.splt()
	for i0 in range(args.start_ip[0], args.end_ip[0] + 1):
		for i1 in range(args.start_ip[1], args.end_ip[1] + 1):
			for i2 in range(args.start_ip[2], args.end_ip[2] + 1):
				for i3 in range(args.start_ip[3], args.end_ip[3] + 1):
					header = icmp.ICMPHeader()
					msg = icmp.ICMPMessage(header)
					ip = str(i0) + "." + str(i1) + "." + str(i2) + "." + str(i3)
					MSGS.append((msg, ip))
					con.send(ip, msg)

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
		self.sip = start_ip
		self.eip = end_ip
		self.start_ip = [int(_) for _ in self.sip.split(".")]
		self.end_ip = [int(_) for _ in self.eip.split(".")]

	def splt(self):
		self.start_ip = [int(_) for _ in self.sip.split(".")]
		self.end_ip = [int(_) for _ in self.eip.split(".")]


def analyse_args():
	args = Args()
	for i, a in enumerate(sys.argv):
		if a == "-s":
			args.sip = sys.argv[i + 1]

		if a == "-e":
			args.eip = sys.argv[i + 1]

		if a == "-f":
			args.file_name = sys.argv[i + 1]

	return args


if __name__ == "__main__":
	args = analyse_args()
	ping_all(args)

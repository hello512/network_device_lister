import subprocess

class Ip:
	def __init__(self, b0 = 0, b1 = 0, b2 = 0, b3 = 0):
		self.b0 = b0
		self.b1 = b1
		self.b2 = b2
		self.b3 = b3

	def __repr__(self):
		return(str(self.b0) + '.' + str(self.b1) + '.' + str(self.b2) + '.' + str(self.b3))



ip = Ip(192, 168, 0, 167)

for i in range(1, 256):
	ret = subprocess.run(['ping', '-c', '1', '192.168.0.' + str(i)], capture_output=True)
	if ret.returncode == 0:
		print('192.168.0.' + str(i) + ' is online')
#	time.sleep(0.1)

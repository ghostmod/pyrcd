import socket
import sys
import os
import time
import threading
import signal

port = 6667
print "server started at port "+str(port)
host = 'localhost'
backlog = 5
size = 1024
all_clients = []

def die():
	os.kill(os.getpid(), signal.SIGINT)

class IRCserver(threading.Thread):
	
	def __init__(self, (sock, addr)):
		self.sock = sock
		self.addr = addr
		self.userinf = {self.sock:{"nick":"","host":"","address":self.addr,"username":"","realname":"","usermodes":"","channels":[]}}
		all_clients.append(sock)
		print addr
		threading.Thread.__init__(self)
		self.startup()
	
	def startup(self):
		self.sock.send("AUTH NOTICE :*** hello there\r\n")
		while 1:
			text = self.sock.recv(size)
			print text
			if text.startswith("NICK"):
				self.userinf[self.sock]["nick"] = text.split("NICK ")[1].split("\n")[0]
				print self.userinf
			if not text:
				die()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, int(port)))
s.listen(2)
threads = []

while True:
	rh = IRCserver(s.accept())
	rh.daemon = True
	rh.start()
	threads.append(rh)
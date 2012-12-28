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
		self.userinf = {"socket":self.sock,"nick":"","host":self.addr[0],"username":"","realname":"","usermodes":"","channels":[]}
		print addr
		threading.Thread.__init__(self)
		self.startup()
	
	def startup(self):
		self.sock.send("AUTH NOTICE :*** hello there\r\n")
		while 1:
			text = self.sock.recv(size)
			print text
			if text.startswith("NICK"):
				nick = text.split('\n')[0]
				user = text.split('\n')[1]
				self.nick = nick.split("NICK ")[1].split("\n")[0]
				self.userinf["nick"] = self.nick
				self.sock.send(":localhost NICK :"+nick.split("NICK ")[1].split("\n")[0]+"\n")
				print self.userinf
			
				self.username = user.split()[1]
				self.realname = user.split(":")[1].split("\n")[0]
				self.userinf["username"] = self.username
				self.userinf["realname"] = self.realname
				print self.userinf
				all_clients.append(self.userinf)
				self.main()
			if not text:
				die()

			
			
	def main(self):
		while 1:
			text = self.sock.recv(size)
			print text
			if text.startswith("JOIN"):
				channel=text.split("JOIN ")[1]
				for x in all_clients:
					print x
					if x["username"] == self.username:
						x["channels"].append(channel)
				self.sock.send(":localhost JOIN :"+channel+"\n")
			
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, int(port)))
s.listen(2)
threads = []

while True:
	rh = IRCserver(s.accept())
	rh.daemon = True
	rh.start()
	threads.append(rh)
import socket
from _thread import *
import sys

host = '127.0.0.1'
port = 6666

serversock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

serversock.bind((host,port))

serversock.listen(5)

def thread_client(conn,player):
	reply=""
	while True:
		try:
			data = conn.recv(2048)
			reply = data.decode("utf-8")

			if not data:
				print("Disconnected")
				break
			else:
				print(reply)
		
			conn.sendall(reply.encode('utf-8'))
		except:
			pass
		
int player=0

while True:
	(CSock, address)= serversock.accept()
	print ("Client Info: ", CSock, address)

	start_new_thread(thread_client,(CSock,),player)
	player+=1

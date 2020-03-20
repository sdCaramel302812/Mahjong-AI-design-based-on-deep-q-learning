import socket,sys
import pickle
import signal
from threading import Thread


class Network(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = "192.168.1.106"
		self.port=6666
		self.addr = (self.server,self.port)
		self.id = self.connect()
		self.setDaemon(True)
		self.start()

	def connect(self):	
		try:
			self.sock.connect(self.addr)
			return self.client.recv(2048).decode('utf-8')
		except:
			pass
	
	def send(self, data):
		self.sock.send(data.encode('utf-8'))

	def close(self):
		self.sock.close()



	def run(self):

#		def exit(*args):
#			n.close()
#			sys.exit(0)


#		signal.signal(signal.SIGTERM, exit)
#		signal.signal(signal.SIGINT, exit)	


		while True:
			data = self.sock.recv(2048*11)
			print('get')
			get_msg=pickle.loads(data)
			if(get_msg[0]=='hand_card'):
				print(get_msg[1])#更新手牌


			if(get_msg[0]=='discard'):
				print(get_msg[1])#摸排 更新14張牌
				draw=input('want to discard:')
				self.send(draw)


			if(get_msg[0]=='chi'):
				print(get_msg[1])
				chi=input('want to chi:')
				self.send(chi)
			
			if(get_msg[0]=='pon'):
				print(get_msg[1])
				pon=input('want to pon:')
				self.send(pon)
			
			if(get_msg[0]=='ron'):
				print(get_msg[1])
				ron=input('want to ron:')
				self.send(ron)

			if(get_msg[0]=='richi'):
				kan=input('want to richi:')
				self.send(kan)

			if(get_msg[0]=='tsumo'):
				tsumo=input('want to tsumo:')
				self.send(tsumo)

			if(get_msg[0]=='kan'):
				print(get_msg[1])
				kan=input('want to kan:')
				self.send(kan)


			if(get_msg[0]=='update'):
				print(get_msg[1])
				print(get_msg[2])
				print(get_msg[3])
				print(get_msg[4])

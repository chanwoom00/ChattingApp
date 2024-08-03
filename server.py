import socket
import threading
import sys 
import argparse
from datetime import datetime, timedelta

active = {}
def start(ip:str, port:int):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((ip, port))
	server.listen(0)
	print(f"Server started on port {port}. Accepting connections")


	sys.stdout.flush()
	return server

def parse():
	parser = argparse.ArgumentParser(prog='server',
									description='create server',
									epilog='create server with port and passcode')
	parser.add_argument("-start", action="store_true", help="start server")
	parser.add_argument("-port", type=int, help="server port number")
	parser.add_argument("-passcode", type=str, help="server passcode (string)")

	args = parser.parse_args()

	if args.start:
		if len(args.passcode.strip()) > 5:
			sys.stdout.flush()
			return -1. -1
		else:
			return args.port, args.passcode
	else:
		sys.stdout.flush()
		return -1, -1

def clients(client, address, passcode, port, username):
	print(f"{username} joined the chatroom")
	sys.stdout.flush()

	#notify clients that new client joined
	for o_client in active.values():
		if o_client != client:
			o_client.send(f"{username} joined the chatroom".encode())

	#add client
	active[username] = client

	while True:
		message = client.recv(1024).decode()
		flagDM = False
		if len(message) > 20:
			continue
		elif message == ":Exit":
			#exit
			print(f"{username} left the chatroom")
			client.close()
			active.pop(username)
			for o_client in active.values():
				if o_client != client:
					o_client.send(f"{username} left the chatroom".encode())
		elif message == ":mytime":
			#time
			time = datetime.now()
			message = str(time.strftime("%a %b %d %H:%M:%S %Y"))
			# print(f'{username}: {message}')
			# sys.stdout.flush()
			# for o_client in active.values():
			# 	if o_client != client:
			# 		o_client.send(f'{username}: {message}'.encode())
			# 		sys.stdout.flush()

		elif message == ":+1hr":
			#+1hr
			time = datetime.now() + timedelta(hours=1)
			message = str(time.strftime("%a %b %d %H:%M:%S %Y"))
			# print(f'{username}: {message}')
			# sys.stdout.flush()
			# for o_client in active.values():
			# 	if o_client != client:
			# 		o_client.send(f'{username}: {message}'.encode())
			# 		sys.stdout.flush()

		elif message[:3] == ":dm": 
			#dm
			flagDM = True
			splitted = message.split(' ', 2)
			rec_username, *dm_message = splitted[1], splitted[2]
			# dummy, rec_username, *dm_message = message.split(' ', 2)
			dm_message = ' '.join(dm_message)
			if rec_username in active:
				receiver = active[rec_username]
				receiver.send(f'{username}: {dm_message}'.encode())
				print(f'{username} to {rec_username}: {dm_message}')
				sys.stdout.flush()

		if not flagDM:
			print(f'{username}: {message}')
			sys.stdout.flush()
			for o_client in active.values():
				if o_client != client:
					o_client.send(f'{username}: {message}'.encode())
					sys.stdout.flush()

port, passcode = parse()
if port != -1:
	#valid port
	server = start("127.0.0.1", port)
	while True:
		client, client_add = server.accept()
		client.send("1".encode())
		client_passcode = client.recv(100).decode()

		#check valid passcode
		if passcode != client_passcode:
			client.send("Incorrect passcode"[:1024].encode())
			client.close()
		else:
			client.send(f"Connected to {client_add[0]} on port {port}"[:1024].encode())
			username = client.recv(1024).decode()
			threading.Thread(target=clients, args=(client, client_add, passcode, port, username)).start()

import socket
import threading
import sys
import argparse
from datetime import datetime, timedelta


def parse():
	parser = argparse.ArgumentParser(prog='server',
									description='setup connection with server',
									epilog='create connection with server with port and passcode')
	parser.add_argument('-join', action='store_true')
	parser.add_argument('-host', type=str)
	parser.add_argument('-port', type=int)
	parser.add_argument('-username', type=str)
	parser.add_argument('-passcode', type=str)

	args = parser.parse_args()

	if args.join:
		if len(args.username.strip()) > 8:
			print("Invalid: Display name longer than 8 characters")
			return -1, -1, -1, -1
		else:
			return args.host, args.port, args.username, args.passcode
	else:
		print("Invalid: -join required")
		return -1, -1, -1, -1

def connect(host, port, username, passcode):
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((host, port))
	status = client.recv(100).decode()

	def receive():
		while open:
			message = client.recv(1024).decode()
			print(message)
			sys.stdout.flush()
	
	if status == str(1):
		client.send(passcode[:100].encode())

		response = client.recv(1024).decode()
		#***
		if response.split(" ")[0] == "Incorrect":
			print(response)
			sys.stdout.flush()
			client.close()
			return
		else:
			print(response)
			sys.stdout.flush()
			client.send(username[:1024].encode())
			open = True
			thread = threading.Thread(target=receive)
			thread.start()

			while True:
				message = input()
				
					
				if message == ":)":
					message = "[feeling happy]"

				elif message == ":(":
					message = "[feeling sad]"

				elif message == ":mytime":
					time = datetime.now()
					print(time.strftime("%a %b %d %H:%M:%S %Y"))
					sys.stdout.flush()

				elif message == ":+1hr":
					time = datetime.now() + timedelta(hours=1)
					print(time.strftime("%a %b %d %H:%M:%S %Y"))
					sys.stdout.flush()

				client.send(message[:1024].encode())
				
				if message == ":Exit":
					open = False
					thread.join()
					client.close()
					return

host, port, username, passcode = parse()
if host != -1:
	connect(host, port, username, passcode)





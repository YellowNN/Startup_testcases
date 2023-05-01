from socket import *
import json
import ipdb


class Client:
	def __init__(self, ip, port):
		self.cli = socket(AF_INET, SOCK_STREAM)
		self.cli.connect((ip, port))

	def connect(self):
		try:
			msg = self.cli.recv(1024).decode('utf-8')
		except Exception as e:
			print(f'ERROR:{str(e)}')
			exit()

		if msg == 'You are connected!':
			self.listen()
		else:
			exit()

	def sender(self,  text):
		self.cli.send(text.encode('utf-8'))
		while self.cli.recv(1024).decode('utf-8') != 'getted':
			self.cli.send(text.encode('utf-8'))

	def listen(self):
		is_work = True
		while is_work:
			req = input(f'What do you want to do? Enter/Show?\n'
				f'(write "disconnect" to leave)\n')
			if req:
				if req == 'disconnect':
					self.sender(req)
					print(self.cli.recv(1024).decode('utf-8'))
					is_work = False

				#ipdb.set_trace()

				if req == 'Enter':
					self.sender(req)
					print(self.cli.recv(1024).decode('utf-8'))

					#минимальная валидация
					validation = 'non pass'
					while validation == 'non pass':
						name, last_name, age, sex = map(str, input().split())
						if age.isdigit() != True:
							print('Please, put age in numbers')
						else:
							validation = 'pass'

					if validation == 'pass':
						data_req = f'{name}, {last_name}, {age}, {sex}'
						self.sender(data_req)
					data = json.loads(
						self.cli.recv(1024).decode('utf-8')
						)
					if data['answer']:
						print(f"SERVER ANSWER:\n\t{data['answer']}")
					elif data['error']:
						print(f"SERVER ANSWER:\n\t{data['error']}")

					
				else:
					self.sender(req)
					data = json.loads(
						self.cli.recv(1024).decode('utf-8')
						)
					if data['answer']:
						print(f"SERVER ANSWER:\n\t{data['answer']}")
					elif data['error']:
						print(f"SERVER ANSWER:\n\t{data['error']}")

Client(input('Type server ip: '), 6000).connect()



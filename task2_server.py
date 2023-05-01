from socket import *
import sqlite3 as sql
import json
import ipdb

class Server:
	def __init__(self, ip, port, base_name):
		print(f'SERVER IP: {ip}\nSERVER PORT: {port}\n')
		self.data_name = base_name
		self.ser = socket(AF_INET, SOCK_STREAM)
		self.ser.bind((ip, port))
		self.ser.listen(3)

	def sender(self, user, text):
		user.send(text.encode('utf-8'))

	def start_server(self):
		while True:
			user, addr = self.ser.accept()
			print(f'CLIENT CONNECTED:\n\tIP: {addr[0]}\n\tPORT: {addr[1]}')
			self.listen(user)

	def listen(self, user):
		self.sender(user, 'You are connected!')
		is_work = True

		while is_work:
			#ipdb.set_trace()
			try:
				data = user.recv(1024)
				self.sender(user, 'getted')
			except Exception as e:
				data = ''
				is_work = False

			if len(data) > 0:

				msg = data.decode('utf-8')
				print(msg)
				if msg == 'disconnect':
					self.sender(user, 'You are disconnected')
					user.close()
					is_work = False

				else:
					con = sql.connect(self.data_name)
					cur = con.cursor()
					cur.execute("CREATE TABLE if not exists users(first_name text, last_name text, age integer, sex text)")
					con.commit()
					
					if msg == 'Enter':
						self.sender(user, f'Please, put your Name, Last name,\n'
									 f'age(numbers) and sex(male/female) to add data into base')
						data_to_DB = user.recv(1024).decode('utf-8')
						print(data_to_DB)
						data_to_ex = list(data_to_DB.split(sep=','))

						cur.execute("INSERT INTO users (first_name, last_name, age, sex) VALUES(?, ?, ?, ?)", 
							(data_to_ex[0],data_to_ex[1],data_to_ex[2],data_to_ex[3]))
						con.commit()

					if msg == 'Show':
						msg = 'select * from users'
					
					try:
						answer = [x for x in cur.execute(msg)]
						error = ''
					except Exception as e:
						error = str(e)
						answer = ''

					con.commit()
					cur.close()
					con.close()

					ans = json.dumps(
						{ 'answer' : answer, 'error' : error }
					)

					self.sender(user, ans)

				data = b''
				msg = ''

			else:
				print('Client disconnected')
				is_work = False

Server('192.168.43.143', 6000, 'data.db').start_server()


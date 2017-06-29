#! /usr/bin/python3

#libraries
import socket, json
import subprocess, sys, shlex
import http, http.client, urllib.parse
import socket
from collections import namedtuple

#from gpiozero import Button, LED
from time import sleep
import time

######################## Initial Setup ###########################

#Server Setup
host = "127.0.0.1"
port = 5005

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = (host,port)
s.bind(server_address)
s.listen(1)
print("Esperando conexao com reconhecimento facial")
connection, client_address = s.accept()
connection.settimeout(0.5)

#Bluetooth Setup
perl = "/usr/bin/perl" #perl path
perl_script = "./bluetooth.pl"	#script path

#Keyboard & Password setup
PASSW_LENGTH = 6
#Keyboard pins
#row_1 = LED(5);  row_2 = LED(6);  row_3 = LED(13); row_4 = LED(19)
#col_1 = Button(26, False, 0.25); col_2 = Button(16, False, 0.25); col_3 = Button(20, False, 0.25); col_4 = Button(21, False, 0.25)

# Connect to RAISE
raise_conn = http.client.HTTPConnection('homol.redes.unb.br')

################### Functions Auto-registro ########################
def register_client():
	params = json.dumps({
	  "name": "ControleAcesso",
	  "chipset": "RaspberryPi3",
	  "mac": "FF:FF:FF:FF:FF:FF",
	  "serial": "C210",
	  "processor": "Intel I3",
	  "channel": "Ethernet",
	  "client_time": 1317427200,
	  "tag": [
	    "controle de acesso",
	    "topicos"
	  ]
	})

	headers = {"content-type": "application/json" , "Accept": "application/json"}
	raise_conn.request("POST", "/uiot-raise/client/register", params, headers)
	sleep(0.5)
	response = raise_conn.getresponse()
	data = json.loads(response.read().decode("utf-8"))
	return data

def revalidate_client(serviceJSON):
	print("Revalidando token")
	params = json.dumps({
		"tokenId" : serviceJSON["tokenId"],
		"services" : [
			serviceJSON["services"][0]["service_id"],
			serviceJSON["services"][1]["service_id"],
			serviceJSON["services"][2]["service_id"]
		]
	})
	headers = {"content-type": "application/json" , "Accept": "application/json"}
	raise_conn.request("POST", "/uiot-raise/client/revalidate", params, headers)
	sleep(0.5)
	response = raise_conn.getresponse()
	data = json.loads(response.read().decode("utf-8"))

	#escrever no arquivo txt o novo tokenId
	serviceJSON["tokenId"] = data["tokenId"]
	service_file = open('servicos.txt','r+')
	service_file.write(json.dumps(serviceJSON))
	service_file.close()
	return serviceJSON


def register_service(clientID):
	params = json.dumps({
	  "services": [
	    {
	      "name": "Cadastro",
	      "parameters": {
	        "name": "string",
	        "password": "string",
	        "MAC": "string",
	      },
	      "return_type": "float"
	    },
	        {
	      "name": "Estado da porta",
	      "parameters": {
	        "state": "bool"
	      },
	      "return_type": "float"
	    },
	    {
	      "name": "Entrada",
	      "parameters": {
	        "name": "string"
	      },
	      "return_type": "float"
	    }
	  ],
	  "tokenId": clientID,
	  "client_time": 1317427200,
	  "tag": [
	    "functions"
	  ]
	})
	headers = {"content-type": "application/json" , "Accept": "application/json"}
	raise_conn.request("POST", "/uiot-raise/service/register", params, headers)
	sleep(0.5)
	response = raise_conn.getresponse()
	data = json.loads(response.read().decode("utf-8"))
	return data

def register_data(clientID,serviceID,dataVal):
	params = json.dumps({
	  "token": clientID,
	  "client_time": 342343242,
	  "tag": [
	    "Cebola"
	  ],
	  "data": [
	    {
	      "service_id": serviceID,
	      "data_values": dataVal
	    }
	  ]
	})
	print(params)
	headers = {"content-type": "application/json" , "Accept": "application/json"}
	raise_conn.request("POST", "/uiot-raise/data/register", params, headers)
	sleep(0.5)
	response = raise_conn.getresponse()
	data = json.loads(response.read().decode("utf-8"))
	return data['code']

def auto_register():
	#Client Request
	client_file = open('cliente.txt','r+')
	client_file_content = client_file.read()
	if(client_file_content==''):
		data = register_client()
		client_file.write(json.dumps(data))
		clientID = data['tokenId']
		print(data['code'], data['message'], data['tokenId'])
	else:
		print("Cliente ja registrado")
		client_JSON = json.loads(client_file_content)
	client_file.close()

	#Service Request
	service_file = open('servicos.txt','r+')
	service_file_content = service_file.read()
	service_JSON = ""
	if(service_file_content==''):
		data = register_service(clientID)
		service_file.write(json.dumps(data))
		servicesID = data['services']
		service_JSON = data
		print(data['code'], data['message'], data['services'])
	else:
		print("Servico ja registrado")
		service_JSON = json.loads(service_file_content)

	service_file.close()
	return service_JSON

def get_data(clientID,serviceID):
	url="/uiot-raise/data/list?"
	url += "tokenId=" + str(clientID)
	url += "&service_id=" + str(serviceID)
	raise_conn.request("GET", url)
	sleep(0.5)
	response = raise_conn.getresponse()
	data = json.loads(response.read().decode("utf-8"))
	#print(data['code'])
	return data



############################# Main ################################

def main():
	nameRecognized = ""

    #teste - servidor fora do ar
	# service_file = open('servicos.txt','r+')
	# service_file_content = service_file.read()
	# services = json.loads(service_file_content)
	# service_file.close()
	# services_dict = services["services"]

	services = auto_register()
	while True:
		try:
			####### PARTE DE CADASTRO
			dataServer=connection.recv(50).decode("utf-8")
			if (len(dataServer) > 0):
				print(dataServer)
				print("Cadastrando usuario")
				i = 0
				pos = 0
				aux = ""
				while(i < len(dataServer)):
					if(dataServer[i] == ';'):
						nome = aux
						break
					aux += dataServer[i]
					i += 1
				i+=1
				aux = ""
				while(i < len(dataServer)):
					if(dataServer[i] == ';'):
						senha = aux
						break
					aux += dataServer[i]
					i += 1
				i+=1
				aux = ""
				bt = ""
				while(i < len(dataServer)):
					bt += dataServer[i]
					i += 1
				dados = {
					"name":nome,
					"password":senha,
					"MAC":bt,
				}
				#enquanto nao for aceito, tenta cadastrar
				while int(register_data(services["tokenId"],services["services"][0]["service_id"],dados)) != 200:
					services = revalidate_client(services)
			else:
				connection.close()
				print("reconhecimento facial desconectado")
				#waitConnection()
				#sleep(0.5)

		except socket.timeout:

			####### CONTINUA NORMALMENTE O CODIGO

			#print("Waiting for password...")

			# passwd = 0
			# passwd = input('Digite sua senha\n')
			passwd = "123456"
			#80:EA:96:D5:FD:D4

			#passwd = get_password()
			#print("Password received:", passwd)

			cadastros = get_data(services["tokenId"],services["services"][0]["service_id"])
			while int(cadastros['code']) != 200:
				services = revalidate_client(services)
				cadastros = get_data(services["tokenId"],services["services"][0]["service_id"])

			cadastros_dict = cadastros["values"]

			passwd_esperado = []
			mac_esperado = []
			name_esperado = []
			#pega todos cadastros que tem a senha digitada e salva num array as informacoes
			for eachPerson in cadastros_dict:
				eachInformation = eachPerson["data_values"]
				if eachInformation['password'] == passwd:
					passwd_esperado.append(eachInformation['password'])
					mac_esperado.append(eachInformation['MAC'])
					name_esperado.append(eachInformation['name'])

			if len(passwd_esperado) != 0:
				print(mac_esperado)
				print(passwd_esperado)
				print(name_esperado)

				# mac_esperado = '2C:F0:A2:B4:3C:2B'
				# passwd_esperado = '123456'
				# name_esperado = "bruno"

				#iterar por cada cadastro procurando pelo bluetooth e reconhecimento
				for i in range(len(passwd_esperado)):
					print("Searching bluetooth...")
					if(check_bluetooth(mac_esperado[i])): #buscar pelo bluetooth esperado
						print("Bluetooth verified")
						if(check_facial(name_esperado[i], services)):	#autenticar o rosto do individuo
							print("Authenticated\nOpen door")
							break

						else:
							print("Facial recognition failed")
					else:
						print("Bluetooth not found!")

				print("Continuacao do loop")
			else:
				print("Ninguem cadastrado com essa senha")

def waitConnection():
	host = "127.0.0.1"
	port = 5005
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_address = (host,port)
	s.bind(server_address)
	s.listen(1)
	print("Esperando conexao com reconhecimento facial")
	connection, client_address = s.accept()
	connection.settimeout(0.5)


def check_facial(expectedName, services):
	print("Checking face...")
	try:
		# client.connect(server_address)
		ask = b"ok"
		connection.sendall(ask)
		nameRecognized = connection.recv(30).decode("utf-8")
		print(nameRecognized)
		if nameRecognized == expectedName:
			dados = {
				"name": nameRecognized,
			}
			print("Postando no servidor quem acabou de entrar")
			while int(register_data(services["tokenId"],services["services"][2]["service_id"],dados)) != 200:
				services = revalidate_client(services)
			return True

		return False

	except socket.timeout:
		print("Erro de conexao")
		return False

def check_bluetooth(expectedMAC):
	pl_script = subprocess.Popen([perl, perl_script], stdout=subprocess.PIPE)
	output = pl_script.communicate()
	BT_json = json.loads(output[0].decode("utf-8"))
	print("Bluetooth(s): ",BT_json)
	for device in BT_json['deviceList']:
		if device['MAC']==expectedMAC:
			return True
	return False




def get_password():
	password = ''
	initial_time = time.time()
	#loop
	while 1:
		#Catching keyboard input
		#Testando primeira linha
		row_1.on()
		row_2.off()
		row_3.off()
		row_4.off()

		if col_1.is_pressed:
			sys.stdout.write("*")
			sys.stdout.flush()
			initial_time=time.time()
			password=password+"1"
		elif col_2.is_pressed:
			sys.stdout.write("*")
			sys.stdout.flush()
			initial_time=time.time()
			password=password+"2"
		elif col_3.is_pressed:
			sys.stdout.write("*")
			sys.stdout.flush()
			initial_time=time.time()
			password=password+"3"
		elif col_4.is_pressed:
			sys.stdout.write("*")
			sys.stdout.flush()
			initial_time=time.time()
			password=password+"A"

		#Testando segunda linha
		row_1.off()
		row_2.on()
		row_3.off()
		row_4.off()

		if col_1.is_pressed:
			sys.stdout.write("*")
			sys.stdout.flush()
			initial_time=time.time()
			password=password+"4"
		elif col_2.is_pressed:
			sys.stdout.write("*")
			sys.stdout.flush()
			initial_time=time.time()
			password=password+"5"
		elif col_3.is_pressed:
			sys.stdout.write("*")
			sys.stdout.flush()
			initial_time=time.time()
			password=password+"6"
		elif col_4.is_pressed:
			sys.stdout.write("*")
			sys.stdout.flush()
			initial_time=time.time()
			password=password+"B"

		#Testando terceira linha
		row_1.off()
		row_2.off()
		row_3.on()
		row_4.off()

		if col_1.is_pressed:
			sys.stdout.write("*")
			sys.stdout.flush()
			initial_time=time.time()
			password=password+"7"
		elif col_2.is_pressed:
			sys.stdout.write("*")
			sys.stdout.flush()
			initial_time=time.time()
			password=password+"8"
		elif col_3.is_pressed:
			sys.stdout.write("*")
			sys.stdout.flush()
			initial_time=time.time()
			password=password+"9"
		elif col_4.is_pressed:
			sys.stdout.write("*")
			sys.stdout.flush()
			initial_time=time.time()
			password=password+"C"

		#Testando quarta linha
		row_1.off()
		row_2.off()
		row_3.off()
		row_4.on()

		if col_1.is_pressed:
			sys.stdout.write("*")
			sys.stdout.flush()
			initial_time=time.time()
			password=password+"*"
		elif col_2.is_pressed:
			sys.stdout.write("*")
			sys.stdout.flush()
			initial_time=time.time()
			password=password+"0"
		elif col_3.is_pressed:
			sys.stdout.write("*")
			sys.stdout.flush()
			initial_time=time.time()
			password=password+"#"
		elif col_4.is_pressed:
			sys.stdout.write("*")
			sys.stdout.flush()
			initial_time=time.time()
			password=password+"D"

		if(len(password)>0 and time.time()-initial_time>10):
			password=''
			print("\nPassword timeout!")
			sys.stdout.flush()
			initial_time=time.time()

		if len(password) == PASSW_LENGTH:
			print('')
			return password

		sleep(0.2)


if __name__ == "__main__":
    main()

#! /usr/bin/python3

import socket, json
import subprocess, sys, shlex
import http, http.client, urllib.parse
from _thread import *

# Connect to RAISe
raise_conn = http.client.HTTPConnection('homol.redes.unb.br')

###################Auto-registro#########################
#Client Request
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
response = raise_conn.getresponse()
data = json.loads(response.read().decode("utf-8"))
print(data)
print(data['code'], data['message'], data['tokenId'])

#Service Request
params = json.dumps({
  "services": [
    {
      "name": "Give personal temperature preference",
      "parameters": {
        "name": "string"
      },
      "return_type": "float"
    },
    {
      "name": "Give personal illumination preference",
      "parameters": {
        "name": "string"
      },
      "return_type": "float"
    },
    {
      "name": "Give door state",
      "parameters": {},
      "return_type": "bool"
    },
    {
      "name": "Who's in the env",
      "parameters": {},
      "return_type": "string []"
    }
  ],
  "tokenId": "bbb2a04f09d08e5b9f0a45b17b383651",
  "client_time": 1317427200,
  "tag": [
    "functions"
  ]
})
raise_conn.request("POST", "/uiot-raise/service/register", params, headers)
response = raise_conn.getresponse()
data = json.loads(response.read().decode("utf-8"))
print(data)
print(data['code'], data['message'])

#Data Request
params = json.dumps({
  "token": "bbb2a04f09d08e5b9f0a45b17b383651",
  "client_time": 342343242,
  "tag": [
    "attributes"
  ],
  "data": [
    {
      "service_id": 0,
      "data_values": {
        "press": 35
      }
    }
  ]
})
raise_conn.request("POST", "/uiot-raise/data/register", params, headers)
response = raise_conn.getresponse()
data = json.loads(response.read().decode("utf-8"))
print(data)
print(data['code'], data['message'])

###################Fim do Auto-Registro#################

# Bluetooth Setup
perl = "/usr/bin/perl" #perl path 
perl_script = "/home/marcusvmaia/Controle_de_Acesso/test.pl"	#script path
bt_count = 1002


#Server Setup
host = '127.0.0.1'
port = 5005
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_conns = []

try:
	s.bind((host, port))
except socket.error as e:
	print(str(e))

s.listen(5)
print('Waiting for connection.')

def threaded_client(conn):
	while True:
		variable = 0
		#data = conn.recv(1024)
		#print(data)
		#conn.send(data)
		#conn.close() #estava gerando um erro [Errno 9] bad file descriptor, reconectando a um socket que foi fechado

#listening
while True:

	conn, addr = s.accept()
	print('connected to: '+addr[0]+':'+str(addr[1]))
	start_new_thread(threaded_client,(conn,))
	client_conns.append(conn) #add to collection of clientes

	#If all peripherals are connected
	if len(client_conns)>1: 
		#client_conns[0].send(str.encode('This is the keyboard\n'))
		#client_conns[1].send(str.encode('This is the camera\n'))
		
		while True:

			####### MAIN ALGORITHM #######
			
			password = client_conns[0].recv(6).decode("utf-8")
			if password!="NOPASS":	#caso senha seja enviada
				print("Senha recebida...")
				print(password)
				#validate password
				#if valid_password:
					#call facial recognition on BT_json["deviceList"][0]["MAC"], BT_json["deviceList"][1]["MAC"]
					#if authenticated OPEN DOOR, else doesn't
			else:										#caso senha nao seja enviada
				if bt_count>1000:
					bt_count = 0
					pl_script = subprocess.Popen([perl, perl_script], stdout=subprocess.PIPE)
					output = pl_script.communicate()
					BT_json = json.loads(output[0].decode("utf-8"))
					print("Bluetooth: ",BT_json)
				else:
					bt_count = bt_count+1

				if len(BT_json["deviceList"]) != 0 :
					print("Existem BTs...\n")
					#call facial recognition on BT_json["deviceList"][0]["MAC"], BT_json["deviceList"][1]["MAC"]
					#if authenticated OPEN DOOR, else doesn't
			
			##### END MAIN ALGORITHM #####
raise_conn.close()

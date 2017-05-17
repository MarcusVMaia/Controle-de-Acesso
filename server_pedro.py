#! /usr/bin/python3

import socket
import sys
import http, http.client, urllib.parse
from _thread import *


# conn = http.client.HTTPConnection("bugs.python.org")
# params = urllib.parse.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})
# headers = {"content-type": "application/json","Accept":"application/json"}
# conn.request("POST", "/cebola", params, headers)
# response = conn.getresponse()
# print(response.status, response.reason)

# Connect to RAISe
conn = http.client.HTTPConnection('homol.redes.unb.br/uiot-raise')

#Auto-registro
#Client Request
params = urllib.parse.urlencode({
  "name": "ControleAcesso",
  "chipset": "AMD 790FX",
  "mac": "FF:FF:FF:FF:FF:FF",
  "serial": "C210",
  "processor": "Intel I3",
  "channel": "Ethernet",
  "client_time": 1317427200,
  "tag": [
    "cebola"
  ]
})
headers = {"content-type": "application/json","Accept":"application/json"}
conn.request("POST", "/client/register", params, headers)
response = conn.getresponse()
print(response.status)
#data = response.read()
#ID = data.token

#Service Request
# params = urllib.parse.urlencode({
#   "services": [
#     {
#       "name": "Get temp",
#       "parameters": {
#         "example_parameter": "float"
#       },
#       "return_type": "float"
#     }
#   ],
#   "tokenId": "4c9adfb96a364c6805b28f90a342b65c",
#   "client_time": 1317427200,
#   "tag": [
#     "Cebola"
#   ]
# })
# conn.request("POST", "", params)
# response = conn.getresponse()
# data = response.read()
# ID = data.token

# #Data Request
# params = urllib.parse.urlencode({
#   "token": "4c9adfb96a364c6805b28f90a342b65c",
#   "client_time": 342343242,
#   "tag": [
#     "Cebola"
#   ],
#   "data": [
#     {
#       "service_id": 0,
#       "data_values": {
#         "press": 35
#       }
#     }
#   ]
# })
# conn.request("POST", "", params)
# response = conn.getresponse()
# data = response.read()
# ID = data.token


host = '127.0.0.1'
port = 5005
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((host, port))
except socket.error as e:
	print(str(e))

s.listen(5)
print('Waiting for connection.')

def threaded_client(conn):
	conn.send(str.encode('Welcome, type your info\n'))

	while True:
		data = conn.recv(1024)
		print(data) #linha adicionada para debugar
		reply = 'Server output: '+ data.decode('utf-8')
		if not data:
			break
		conn.send(data)
		#conn.close() estava gerando um erro [Errno 9] bad file descriptor, reconectando a um socket que foi fechado

while True:

	conn, addr = s.accept()
	print('connected to: '+addr[0]+':'+str(addr[1]))

	start_new_thread(threaded_client,(conn,))

raise_conn.close()

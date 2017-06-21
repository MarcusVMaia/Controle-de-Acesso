#! /usr/bin/python3

#libraries
import socket, json
import subprocess, sys, shlex
import http, http.client, urllib.parse
import socket
from time import sleep
import time

# Connect to RAISe
raise_conn = http.client.HTTPConnection('homol.redes.unb.br')

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
	headers = {"content-type": "application/json" , "Accept": "application/json"}
	raise_conn.request("POST", "/uiot-raise/data/register", params, headers)
	sleep(0.5)
	response = raise_conn.getresponse()
	data = json.loads(response.read().decode("utf-8"))
	return data

#Load tokens
service_file = open('servicos.txt','r+')
service_file_content = service_file.read()
services = json.loads(service_file_content)
service_file.close()

print("################# CADASTRO DE USUARIO ###################")

while True:
	nome = input('Digite seu nome\n')
	senha = input('Digite sua senha\n')
	bt = input('Digite seu bluetooth\n')
	uri = input('Digite sua URI\n')

	dados = {
		"name":nome,
		"password":senha,
		"MAC":bt,
		"faceURI":uri
	}

	print(register_data(services["tokenId"],services["services"][0]["service_id"],dados))
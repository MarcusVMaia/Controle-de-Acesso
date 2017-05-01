#! /usr/bin/python

import socket
import sys
import httplib, urllib
from thread import *

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
		print data
		reply = 'Server output: '+ data.decode('utf-8')
		if not data:
			break
		conn.send(data)
		#conn.close() estava gerando um erro [Errno 9] bad file descriptor, reconectando a um socket que foi fechado

while True:

	conn, addr = s.accept()
	print('connected to: '+addr[0]+':'+str(addr[1]))

	start_new_thread(threaded_client,(conn,))

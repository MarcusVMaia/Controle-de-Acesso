#!/usr/bin/env python

#libraries
import socket
from gpiozero import Button

#setup
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

#Keyboard pins
row_1 = Button(5);  row_2 = Button(6);  row_3 = Button(13); row_4 = Button(19)
col_1 = Button(26); col_2 = Button(16); col_3 = Button(20); col_4 = Button(21)

#Connect to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

################### Parte Keyboard ##################
password = ''

def add_digit(dig):
	if len(password) == 6:
		#authenticate
		s.send(password)
		password = '';
		print "Autenticando..."
	else:
		password = password+dig
		print password

#loop
while 1:

	#Catching keyboard input
	if row_1.is_pressed:
		if col_1.is_pressed:
			add_digit('1')
		elif col_2.is_pressed:
			add_digit('2')
		elif col_3.is_pressed:
			add_digit('3')
		elif col_4.is_pressed:
			add_digit('A')
		else:
			print "Pressione novamente"
	elif row_2.is_pressed:
		if col_1.is_pressed:
			add_digit('4')
		elif col_2.is_pressed:
			add_digit('5')
		elif col_3.is_pressed:
			add_digit('6')
		elif col_4.is_pressed:
			add_digit('B')
		else:
			print "Pressione novamente"
	elif row_3.is_pressed:
		if col_1.is_pressed:
			add_digit('7')
		elif col_2.is_pressed:
			add_digit('8')
		elif col_3.is_pressed:
			add_digit('9')
		elif col_4.is_pressed:
			add_digit('C')
		else:
			print "Pressione novamente"
	elif row_4.is_pressed:
		if col_1.is_pressed:
			add_digit('*')
		elif col_2.is_pressed:
			add_digit('0')
		elif col_3.is_pressed:
			add_digit('#')
		elif col_4.is_pressed:
			add_digit('D')
		else:
			print "Pressione novamente"
	#else:
######################################################
	#data = s.recv(BUFFER_SIZE)
s.close()
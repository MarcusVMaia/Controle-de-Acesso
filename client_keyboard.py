#!/usr/bin/env python

#libraries
import socket
from gpiozero import Button, LED
from time import sleep

#Client setup
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

#Keyboard & Password setup
PASSW_LENGTH = 6

#Keyboard pins
row_1 = LED(5);  row_2 = LED(6);  row_3 = LED(13); row_4 = LED(19)
col_1 = Button(26, False, 0.25); col_2 = Button(16, False, 0.25); col_3 = Button(20, False, 0.25); col_4 = Button(21, False, 0.25)

#Connect to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

################### Parte Keyboard ##################
password = ""

def add_digit(dig):
	global password
	if len(password) == PASSW_LENGTH - 1:
		password = password+dig
		#authenticate
		s.send(str.encode(password))
		password = "";
		print "Autenticando..."
	else:
		password = password+dig
		print password
	sleep(0.25)

#loop
while 1:
	#Catching keyboard input
	#Testando primeira linha
	row_1.on()
	row_2.off()
	row_3.off()
	row_4.off()
	
	if col_1.is_pressed:
		add_digit("1")
	elif col_2.is_pressed:
		add_digit("2")
	elif col_3.is_pressed:
		add_digit("3")
	elif col_4.is_pressed:
		add_digit("A")
	
	#Testando segunda linha
	row_1.off()
	row_2.on()
	row_3.off()
	row_4.off()
	
	if col_1.is_pressed:
		add_digit("4")
	elif col_2.is_pressed:
		add_digit("5")
	elif col_3.is_pressed:
		add_digit("6")
	elif col_4.is_pressed:
		add_digit("B")

	#Testando terceira linha
	row_1.off()
	row_2.off()
	row_3.on()
	row_4.off()
	
	if col_1.is_pressed:
		add_digit("7")
	elif col_2.is_pressed:
		add_digit("8")
	elif col_3.is_pressed:
		add_digit("9")
	elif col_4.is_pressed:
		add_digit("C")

	#Testando quarta linha
	row_1.off()
	row_2.off()
	row_3.off()
	row_4.on()
	
	if col_1.is_pressed:
		add_digit("*")
	elif col_2.is_pressed:
		add_digit("0")
	elif col_3.is_pressed:
		add_digit("#")
	elif col_4.is_pressed:
		add_digit("D")
######################################################
	#data = s.recv(BUFFER_SIZE)
s.close()

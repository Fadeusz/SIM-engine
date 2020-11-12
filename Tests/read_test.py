import serial

import time

SERIAL_PORT = "/dev/ttyS0"

ser = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 0.5)

def SendLine(line, wait = True):
	ser.write(str.encode(line + "\r"))
	s = ""
	if(wait == True):
		while 1:
			ch = ser.read();
			print(">" + str(ch) + "<")
			
			if len(ch) == 0:
				break
			s += ch.decode()

			print(ord(ch))
		#print(s)
	s = s.split("\r\r\n")
	s.pop(0)
	s = "\n".join(s)
	s = s.rstrip(chr(10))
	s = s.rstrip(chr(13))
	return s
		#TODO: Zapisywac to co sie tu wypisze jako listy danych a potem te listy czytac jako piorytet podczas sprwadzania nowych danych w petli
		#CEL ^ zeby podczas zbierania informacji tutuaj typu "OK" nie przyszedl miedzyczasie jakis np SMS, z ktorym nic sie nie zrobi

print(":::"+SendLine("AT")+":::")
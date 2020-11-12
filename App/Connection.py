import serial

import time

SERIAL_PORT = "/dev/ttyS0"

ser = serial.Serial(SERIAL_PORT, baudrate = 115200, timeout = 0.5)

SendLineInProgress = False

def SendLine(line, wait = True, onlyFirstLine=False, arrBytes=False):
	global SendLineInProgress
	ser.write(str.encode(line + "\r"))
	s = ""
	bts = bytearray()

	if(wait == True):
		SendLineInProgress = True
		if arrBytes:
			time.sleep(3)

		while 1:
			ch = ser.read();
			#print(">" + str(ch) + "<")
			#print(ord(ch))
			#if len(ch) == 0 or ch == "" or ch == "\n" or ord(ch) == 10:
			if len(ch) == 0:
				break
			if arrBytes:
				bts.append(ord(ch))
				#bts.append(ord(ch))
			else:
				s += ch.decode()
		print(s)
		SendLineInProgress = False
	
		if arrBytes:
			return bts

		s = s.split("\r\r\n")
		s.pop(0)
		s = "\n".join(s)
		s = s.rstrip(chr(10))
		s = s.rstrip(chr(13))
		
		if onlyFirstLine is True:
			return s.split("\n").pop(0)

	return s
		#TODO: Zapisywac to co sie tu wypisze jako listy danych a potem te listy czytac jako piorytet podczas sprwadzania nowych danych w petli
		#CEL ^ zeby podczas zbierania informacji tutuaj typu "OK" nie przyszedl miedzyczasie jakis np SMS, z ktorym nic sie nie zrobi

def Read():
	return ser.read()

def ReadLine():
	return ser.readline()

def Write(s, encode = True):
	if encode == True:
		return ser.write(s.encode())
	else:
		return ser.write(s)
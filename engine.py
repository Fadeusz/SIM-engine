# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import serial
import time,sys
import re
import binascii
import threading

SERIAL_PORT = "/dev/ttyS0"

ser = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 0.5)


def SendLine(line):
	ser.write(line + "\r")

print "Configuration is in progress"

SendLine("AT") #Connect

SendLine("ATS0=1") #Automatic connection reception
SendLine("AT+DDET=1,100,0,0") #Tone Dialling
SendLine("AT+CRSL=0") #Call volume 0
SendLine("AT+CLIP=1") #Caller info
SendLine("AT+CNMI=1,2,0,0,0") #show the content of the incoming message
SendLine('AT+CSCS="UCS2"') #encoding the message to UCS2  ##If it is turned off and the message comes with a sign from off-pallets - it encodes anyway. It is better to make sure that it always encodes.
SendLine("AT+CMGF=1")
#SendLine("AT+CSAS=0") # for CSMP work...s
SendLine("AT+CSMP=17,167,2,25") #utf8 etc...

#Configure GPS
SendLine("AT+CGNSPWR=1")
SendLine("AT+CGATT=1")
SendLine('AT+SAPBR=3,1,"CONTYPE","GPRS"')
SendLine('AT+CGNSSEQ="RMC"')
SendLine("AT+CGPSRST=0")


time.sleep(5)
print "Engine is READY"

def utf16_encode(text):
	return binascii.hexlify(text.encode('utf-16-be'))

class SMS_Send:

	@staticmethod
	def Send(number, text):
		SendLine("AT+CMGF=1") #Configure SMS Format (?)
		ser.write('AT+CMGS="'+utf16_encode(number)+'"\r')
		time.sleep(3)
		ser.write(text + chr(26))
		time.sleep(3)

	#@staticmethod
	queue = []

	@staticmethod
	def add_to_queue(number, text):
		SMS_Send.queue.append([number, utf16_encode(text)])

	@staticmethod
	def send_first():
		ar = SMS_Send.queue.pop(0)
		SMS_Send.Send(ar[0], ar[1])



class SMS_Received:
	inProgress = True

	msg = ""
	number = ""
	date = ""

	def string_decode(self, line):
		return binascii.unhexlify(line.strip()).decode('utf-16-be')

	def __init__(self, line):
		#// +CMT: "+48884167733","","20/09/22,23:12:27+08"
		data = line.split('"')
		self.number = self.string_decode(data[1])
		self.date = data[5]
	def add_line(self, line):
		print "SMS LINE: " + line
		self.msg += self.string_decode(line)
		#self.msg = line
	def make(self):
		self.inProgress = False
		print "Saving sms..."
		print "Time: " + self.date
		print "Sender: " + self.number
		print "Value: " + self.msg
		#Send_SMS("884167733", self.msg)
		#SMS_Send.add_to_queue("884167733", self.msg)
		#SendLine("AT+CGNSINF")
		#SMS_Send.Send(self.number, self.msg);
		self.manager()
	def manager(self):
		if self.msg.startswith("#location"):
			GPS.awaiting_location_list.append(self.number)
			SendLine("AT+CGNSINF")
		elif self.msg.startswith("#pl"): SMS_Send.add_to_queue(self.number, u"Zażółć gęślą jaźń")
		elif self.msg.startswith("#"): SMS_Send.add_to_queue(self.number, "Undefined Command")


class GPS:
	@staticmethod
	def get_position(line):
		args = line.split(",")
		return args[3] + "," + args[4]

	awaiting_location_list = []

	@staticmethod
	def do_list(line):
		position =  GPS.get_position(line)
		if position != ",":
			msg = "https://www.google.com/maps/place/" + position
		else:
			msg = "Location Not Avaiable"

		while len(GPS.awaiting_location_list) > 0:
			nr = GPS.awaiting_location_list.pop(0)
			SMS_Send.add_to_queue(nr, msg)


def ReadSerial(s):
	global Current_Caller

	print "READ:"

	Received_SMS = False

	#def ProcessData():
		#if Received_SMS and Received_SMS.inProgress: Received_SMS.make()

	lines = s.split("\n")
	while "" in lines: lines.remove("")
	while len(lines)>0:
		line = lines.pop(0)
		print "Line: " + line

		if line.startswith("+CGNSINF:"):
			print "GPS:"
			GPS.do_list(line)
		elif line.startswith("+CMT:"):
			Received_SMS = SMS_Received(line)


		#CALL
		elif line.startswith("+CLIP:"):
			l = line.split('"')
			Current_Caller = l[1]
			print "Nawiazono polaczenie z: " + Current_Caller
		elif line.startswith("NO CARRIER"):
			print " ------> Rozmowa zakonczona z numerem: " + Current_Caller
			Current_Caller = 0
		elif line.startswith("+DTMF:"):
			tone = int(line.split(": ")[1])
			print "TONE DIALLING: [" + Current_Caller + "] - [" + str(tone) + "]"


		else:
			if Received_SMS and Received_SMS.inProgress: 
				Received_SMS.add_line(line)
				Received_SMS.make()

	#ProcessData()

while 1:
	s=""

	if len(SMS_Send.queue) > 0:
		SMS_Send.send_first()

	while 1:
		ch = ser.read();
		if ch == "" or ch == "\n\n":
			if s != "":
				#ReadSerial(s)
				thr = threading.Thread(target=ReadSerial, args=(s,))
				thr.start()
			break

		s = s + ch
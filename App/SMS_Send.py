from App.UTF16 import UTF16
from App.Connection import SendLine, Write, Read, ReadLine
import time

class SMS_Send:

	@staticmethod
	def Send(number, text):
		SendLine("AT+CMGF=1") #Configure SMS Format (?)
		Write('AT+CMGS="'+UTF16.encode(number)+'"\r')
		time.sleep(3)
		Write(UTF16.encode(text) + chr(26))
		s = ReadLine()
		print("Status:")
		print(s)
		s = ReadLine()
		print("Status:")
		print(s)
		s = ReadLine()
		print("Status:")
		print(s)
		s = ReadLine()
		print("Status:")
		print(s)
		s = ReadLine()
		print("Status:")
		print(s)
		s = ReadLine()
		print("Status:")
		print(s)
		s = ReadLine()
		print("Status:")
		print(s)
		s = ReadLine()
		print("Status:")
		print(s)
		s = ReadLine()
		print("Status:")
		print(s)
		s = ReadLine()
		print("Status:")
		print(s)
		s = ReadLine()
		print("Status:")
		print(s)
		s = ReadLine()
		print("Status:")
		print(s)

	#@staticmethod
	queue = []

	@staticmethod
	def add_to_queue(number, text):
		SMS_Send.queue.append([number, text])

	@staticmethod
	def send_first():
		ar = SMS_Send.queue.pop(0)
		SMS_Send.Send(ar[0], ar[1])
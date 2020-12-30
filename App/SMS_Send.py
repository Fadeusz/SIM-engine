from App.UTF16 import UTF16
from App.Connection import SendLine, Write, Read, ReadLine, ReadToQueue
import time

class SMS_Send:

	@staticmethod
	def Send(number, text):

		print("SEND SMS: " + text)
		SendLine("AT+CMGF=1") #Configure SMS Format (?)
		ReadToQueue()
		Write('AT+CMGS="'+UTF16.encode(number)+'"\r')
		time.sleep(3)
		ReadToQueue()
		Write(UTF16.encode(text) + chr(26))
		time.sleep(3)

		SendLine("AT")#test

		SMS_Send.LastSend = time.time()

	#@staticmethod
	queue = []

	@staticmethod
	def add_to_queue(number, text, user_id=0):
		print("SMS to queue: " + str(number))
		print("SMS QUEUE: " + str(len(SMS_Send.queue)) )
		SMS_Send.queue.append([number, text, user_id])

	@staticmethod
	def send_first():
		ar = SMS_Send.queue.pop(0)
		SMS_Send.Send(ar[0], ar[1])
		return ar

	LastSend = 0

	@staticmethod
	def Ready_For_Next_SMS():
		res = ( time.time() - SMS_Send.LastSend ) > 60

		if res == False: print("jeszcze nie czas na sms!")

		return res

	@staticmethod
	def Reset_Time():
		SMS_Send.LastSend = 0
		
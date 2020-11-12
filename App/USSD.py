import configparser

from App.Connection import SendLine
from App.SMS_Send import SMS_Send
from App.UTF16 import UTF16

class Config:
	file = ''
	def __init__(self):
		self.file = configparser.RawConfigParser()
		self.file.read("Config/config.ini")

class USSD:

	queue = []

	principal = ""

	@staticmethod
	def Send(number, code):
		conf = Config()
		numbers = conf.file.get("USSD", "admin").split(",")
		if number in numbers:
			if USSD.principal == "":
				USSD.principal = number
				SendLine(u"ATD" + code + ";", False)
			else:
				USSD.queue.append([number, code])
		else:
			SMS_Send.add_to_queue(number, "USSD: Access Denied")

	@staticmethod
	def Get(line):
		if '"' in line:
			msg = line.split('"')[1]
			message = UTF16.decode(msg)
			SMS_Send.add_to_queue(USSD.principal, "USSD Code: \n--------\n" + message)
			USSD.principal = ""
			if len(USSD.queue) > 0:
				q = USSD.queue.pop(0)
				USSD.Send(q[0], q[1])
		else:
			print("E1")
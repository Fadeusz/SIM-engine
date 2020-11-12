import time

from App.UTF16 import UTF16
from App.SMS_Send import SMS_Send
from App.MMS_Send import MMS_Send
from App.GPS import GPS
from App.Connection import SendLine
from App.USSD import USSD

class SMS_Received:
	inProgress = True

	msg = ""
	number = ""
	date = ""

	def __init__(self, line):
		print("SSM INIT")
		#// +CMT: "+48884167733","","20/09/22,23:12:27+08"
		data = line.split('"')
		self.number = UTF16.decode(data[3].strip())
		self.date = data[7]
	def add_line(self, line):
		print("SMS LINE: " + line)
		self.msg += UTF16.decode(line.strip())
		#self.msg = line
	def make(self):
		self.inProgress = False
		print("Saving sms...")
		print("Time: " + self.date)
		print("Sender: " + self.number)
		print("Value: " + self.msg)
		#Send_SMS("884167733", self.msg)
		#SMS_Send.add_to_queue("884167733", self.msg)
		#SendLine("AT+CGNSINF")
		#SMS_Send.Send(self.number, self.msg);

		fn = self.date.replace("/","-").replace(":", "-") + "___" + str(time.time())

		f = open("Data/Received_SMS/msg_" + fn + ".txt", "w+")
		f.write(self.date + "\n")
		f.write(self.number + "\n")
		f.write(self.msg)
		f.close()

		self.manager()
	def manager(self):
		if self.msg.startswith("#location"):
			GPS.awaiting_location_list.append(self.number)
			SendLine("AT+CGNSINF", False)
		elif self.msg.startswith("#pl"): SMS_Send.add_to_queue(self.number, u"Zażółć gęślą jaźń")
		#elif self.msg.startswith("#"): SMS_Send.add_to_queue(self.number, "Undefined Command")
		elif self.msg.startswith("#ussd"):
			time.sleep(5)
			USSD.Send(self.number, self.msg.split(" ")[1])
		elif self.msg.startswith("#mms"):
			MMS_Send.add_to_queue(self.number, ["fff.jpg"])
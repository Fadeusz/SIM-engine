import threading
from App.SMS_Send import SMS_Send
from App.MMS_Send import MMS_Send
from App.ReadSerial import ReadSerial
import App.Connection

import time

def Loop():
	print("Loop Started!")
	while 1:
		s=""

		if len(SMS_Send.queue) > 0:
			SMS_Send.send_first()

		if len(MMS_Send.queue) > 0:
			MMS_Send.send_first()

		while 1:

			if App.Connection.SendLineInProgress == True:
				#print("loop skipped..")
				time.sleep(0.5)
				continue

			ch = App.Connection.Read();
			if len(ch) == 0 or ch == "" or ch == "\n" or ord(ch) == 10:
				if s != "":
					#ReadSerial(s)
					thr = threading.Thread(target=ReadSerial, args=(s,))
					thr.start()
				break

			#print(ch)
			try:
				s += ch.decode('windows-1252')
				#s += ch.decode()
			except:
				print("! decode char except")
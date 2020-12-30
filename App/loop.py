import threading
from App.SMS_Send import SMS_Send
from App.MMS_Send import MMS_Send
from App.ReadSerial import ReadSerial
import App.Connection
from App.SQL import SQL
import App.Config

import time

from App.WebSocket import WebSocketClient_Send

def Loop():

	#App.Config.SQL = SQL()


	print("Loop Started!")
	while 1:
		s=""

		if len(SMS_Send.queue) > 0 and SMS_Send.Ready_For_Next_SMS():
			ar = SMS_Send.send_first()
			App.WebSocket.WebSocketClient_Send({"action":"SmsSentStatus", "status": "1", "ar":ar})

		if len(MMS_Send.queue) > 0:
			MMS_Send.send_first()

		if len(App.Connection.ReadQueue) > 0:
			print("Using ReadQueue pop.")
			ReadSerial(App.Connection.ReadQueue.pop(0))
			continue

		while 1:

			if App.Connection.SendLineInProgress == True:
				#print("loop skipped..")
				time.sleep(0.5)
				continue

			ch = App.Connection.Read();


			#if len(ch) == 0: break

			#if len(ch) != 0: 
				#print(str(ord(ch)) + " -> " + ch.decode() )
			#else:
				#print("empty") 
				#break



			#if len(ch) == 0 or ch == "" or ch == "\n" or ord(ch) == 10:
			#if ord(ch) == 10:
			if len(ch) == 0:
				if s != "":
					ReadSerial(s)
					#thr = threading.Thread(target=ReadSerial, args=(s,))
					#thr.start()
				break

			try:
				s += ch.decode('windows-1252')
				#s += ch.decode()
			except:
				print("! decode char except")
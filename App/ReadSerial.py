import time

from App.SMS_Received import SMS_Received
from App.GPS import GPS
from App.USSD import USSD
from App.Connection import SendLine
from App.Audio import play
from App.Config import ToneDialing
import App.Config
from App.WebSocket import WebSocketClient_Send
from App.MMS_Received import MMS_Received
from App.SMS_Send import SMS_Send
import App.Logs

Received_SMS = False
Received_MMS = False
Wait_For_MMS = False

import re
import PIL.Image as Image
from io import StringIO

def ReadSerial(s):
	global Conversation_Progress
	global Received_SMS
	global Received_MMS
	global Wait_For_MMS

	print("READ:" + s)

	#def ProcessData():
		#if Received_SMS and Received_SMS.inProgress: Received_SMS.make()

	lines = s.split("\n")
	while "" in lines: lines.remove("")
	while len(lines)>0:
		line = lines.pop(0)
		print("Line: " + line)

		App.Logs.Serial(line)


		if Wait_For_MMS:
			if line.startswith("+CMMSRECV:"):
				Wait_For_MMS = False
				while len(App.Config.MMSQueue) > 0: App.Connection.ReadQueue.append(App.Config.MMSQueue.pop(0))
			else:
				print("I am already reading another MMS")
				App.Config.MMSQueue.append(line)
				continue

		#GPS DATA
		if line.startswith("+CGNSINF:"): GPS.do_list(line)


		#READ SMS
		elif line.startswith("+CMGR:"): Received_SMS = SMS_Received(line)
		#elif line.startswith("+CMT:"): Received_SMS = SMS_Received(line)


		#SIM OPERATOR CODE
		elif line.startswith("+CUSD:"): USSD.Get(line)
			
		#informacja o wyslanym sms
		#elif line.startswith("+CMGS:"): WebSocketClient_Send({"action":"addNotification", "log":"smsSent", "level": "2"})
		elif line.startswith("+CMGS:"): 
			WebSocketClient_Send({"action":"SmsSentStatus", "status": "3"})
			SMS_Send.Reset_Time()

		#elif line.startswith("+CMS ERROR:"): WebSocketClient_Send({"action":"addNotification", "log":"smsSentError", "level": "0"})
		elif line.startswith("+CMS ERROR:"): 
			WebSocketClient_Send({"action":"SmsSentStatus", "status": "2"})
			SMS_Send.Reset_Time()

		#przyszedl nowy mms lub sms
		elif line.startswith("+CMTI:"):
			l = line.split(",")
			print("Reading SMS/MMS message...")
			if len(l) > 2 and "MMS PUSH" in l[2]:

				SendLine("AT+SAPBR=1,1")
				time.sleep(2)
				SendLine("AT+SAPBR=2,1")
				time.sleep(2)
				SendLine("AT+CMMSRECV=" + l[1])
				Wait_For_MMS = True
			else:
				SendLine("AT+CMGR=" + l[1], False)



		elif line.startswith("+CMMSRECV:"):
			Received_MMS = MMS_Received(line)

		#CALL
		elif line.startswith("+CLIP:"):
			l = line.split('"')
			App.Config.Current_Caller = l[1]

			SendLine("ATA", False)

			print("Nawiazono polaczenie z: " + App.Config.Current_Caller)
			ToneDialing.Reset()
			ToneDialing.Run()

		#end call
		elif line.startswith("NO CARRIER"):
			print(" ------> Rozmowa zakonczona z numerem: " + App.Config.Current_Caller)
			App.Config.Current_Caller = 0
			if App.Config.Micro.stopped == False:
				WebSocketClient_Send({"action":"TerminateConversation"})
			App.Config.Micro.stop();

		#select tone dial
		#TODO
		#tutaj raczej trzeba dolozyc tworzenie nowego watku, o ile ReadSerial nie jest juz nowym watkiem
		elif line.startswith("+DTMF:"):
			tone = int(line.split(": ")[1])
			print("TONE DIALLING: [" + App.Config.Current_Caller + "] - [" + str(tone) + "]")
			ToneDialing.Click(str(tone))

		else:
			if Received_SMS != False and Received_SMS.inProgress: 
				Received_SMS.add_line(line)
				Received_SMS.make()

			elif Received_MMS != False:
				pattern = re.compile('^\d+,"[^"]{0,}",\d+,\d+[\n\r]*$')
				if pattern.match(line):
					Received_MMS.add_file(line)
				else:
					#print("its not mms line!")
					Received_MMS = False

			#else:
				#print("Loop ELSE '"+line+"'")

	#ProcessData()
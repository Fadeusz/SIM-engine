import time

from App.SMS_Received import SMS_Received
from App.GPS import GPS
from App.USSD import USSD
from App.Connection import SendLine
from App.Audio import play
from App.Config import ToneDialing
import App.Config
from App.WebSocket import WebSocketClient_Send
Received_SMS = False
Check_MMS = False

import re
import PIL.Image as Image
from io import StringIO

def ReadSerial(s):
	global Conversation_Progress
	global Received_SMS
	global Check_MMS

	#print("READ:")

	#def ProcessData():
		#if Received_SMS and Received_SMS.inProgress: Received_SMS.make()

	lines = s.split("\n")
	while "" in lines: lines.remove("")
	while len(lines)>0:
		line = lines.pop(0)
		print("Line: " + line)

		#GPS DATA
		if line.startswith("+CGNSINF:"): GPS.do_list(line)


		#READ SMS
		elif line.startswith("+CMGR:"): Received_SMS = SMS_Received(line)
		#elif line.startswith("+CMT:"): Received_SMS = SMS_Received(line)


		#SIM OPERATOR CODE
		elif line.startswith("+CUSD:"): USSD.Get(line)
			
		
		elif line.startswith("+CMGS:"): WebSocketClient_Send({"action":"addNotification", "log":"smsSent", "level": "2"})

		elif line.startswith("+CMTI:"):
			l = line.split(",")
			
			if len(l) > 2 and "MMS PUSH" in l[2]:
				SendLine("AT+SAPBR=1,1", False)
				time.sleep(2)
				SendLine("AT+SAPBR=2,1", False)
				time.sleep(2)
				SendLine("AT+CMMSRECV=" + l[1], False)
			else:
				SendLine("AT+CMGR=" + l[1], False)



		elif line.startswith("+CMMSRECV:"):
			print("Sprawdzam zalaczniki MMSA....")
			Check_MMS = True

		#CALL
		elif line.startswith("+CLIP:"):
			l = line.split('"')
			App.Config.Current_Caller = l[1]

			SendLine("ATA", False)

			print("Nawiazono polaczenie z: " + App.Config.Current_Caller)
			ToneDialing.Reset()
			ToneDialing.Run()

			#Conversation_Progress = 0
			#time.sleep(1)
			#play("powitanie")
		elif line.startswith("NO CARRIER"):
			print(" ------> Rozmowa zakonczona z numerem: " + App.Config.Current_Caller)
			App.Config.Current_Caller = 0
			if App.Config.Micro.stopped == False:
				WebSocketClient_Send({"action":"TerminateConversation"})
			App.Config.Micro.stop();
		elif line.startswith("+DTMF:"):
			tone = int(line.split(": ")[1])
			print("TONE DIALLING: [" + App.Config.Current_Caller + "] - [" + str(tone) + "]")
			ToneDialing.Click(str(tone))
			#if tone == 1 and Conversation_Progress == 0:
				#play("1_0")
				#SendLine("ATH", False)


		else:
			if Received_SMS != False and Received_SMS.inProgress: 
				Received_SMS.add_line(line)
				Received_SMS.make()

			elif Check_MMS != False:
				pattern = re.compile('^\d+,"[^"]{0,}",\d+,\d+[\n\r]*$')
				if pattern.match(line):
					print("MMS LINE: " + line)
					l = line.split(",")
					if(l[1] != '""'):
						print("Saving MMS image...")
						img = SendLine("AT+CMMSREAD=" + l[0], arrBytes=True)
						newFile = open("Data/test2.jpg", "wb")
						newFile.write(img)
						print("MMS saved.")
					else:
						print("EMPTY MMS!!!!!!!!!!")
				else:
					print("its not mms line!")
					Check_MMS = False

			#else:
				#print("Loop ELSE '"+line+"'")

	#ProcessData()
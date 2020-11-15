from App.Connection import SendLine
import App.Config

from App.Controller_Configuration import Controller_Configuration
import hashlib

import json
import io

from App.ToneDialing import ToneDialing

import time

class Init:
	def __init__(self):
		self.AT()
		self.Config()

	def AT(self):

		#return print("Ignore init!")

		print("Configuration is in progress")

		SendLine("AT") #Connect

		SendLine("AT+CMEE=2") #show errors


		SendLine('AT+CMGDA="DEL ALL"')

		App.Config.SN = SendLine("AT+GSN", onlyFirstLine=True)

		print("SN: " + App.Config.SN)
		result = hashlib.sha256(App.Config.SN.encode())
		App.Config.unique_id = result.hexdigest()
		print("u_id: " + App.Config.unique_id)

		SendLine("ATS0=0") #Automatic connection reception - FALSE
		SendLine("AT+DDET=1,100,0,0") #Tone Dialling
		SendLine("AT+CRSL=0") #Call volume 0
		SendLine("AT+CLIP=1") #Caller info
		#SendLine("AT+CNMI=1,2,0,0,0") #show the content of the incoming message
		SendLine('AT+CSCS="UCS2"') #encoding the message to UCS2  ##If it is turned off and the message comes with a sign from off-pallets - it encodes anyway. It is better to make sure that it always encodes.
		SendLine("AT+CMGF=1")
		SendLine("AT+CSAS=0") # for CSMP work...s
		SendLine("AT+CSMP=17,167,2,25") #utf8 etc...

		SendLine("AT+CUSD=1") #card  operator message

		#Configure GPS
		SendLine("AT+CGNSPWR=1")
		SendLine("AT+CGATT=1")
		SendLine('AT+SAPBR=3,1,"CONTYPE","GPRS"')
		SendLine('AT+CGNSSEQ="RMC"')
		SendLine("AT+CGPSRST=0")

		#MMS
		SendLine('AT+CMMSINIT')
		time.sleep(1)
		SendLine('AT+CMMSCURL="mms.orange.pl"')
		time.sleep(1)
		SendLine('AT+CMMSCID=1')
		time.sleep(1)
		SendLine('AT+CMMSPROTO="192.168.6.104",8080')
		time.sleep(1)
		SendLine('AT+SAPBR=3,1,"Contype","GPRS"')
		time.sleep(1)
		SendLine('AT+SAPBR=3,1,"APN","mms"')


		print("Engine is READY")


	def Config(self):
		App.Config.Controller = Controller_Configuration()
		App.Config.Controller.Login()

		try:
			f = open("Config/ToneDialing.json", "r")
			c = f.read()
			ToneDialingString = io.StringIO(c)
			App.Config.ToneDialing = ToneDialing()
			App.Config.ToneDialing.Configure(json.load(ToneDialingString))
			print("Tone Dialing Ready!")
		except:
			print("[!] Tone Dialing: Wrong Data")

		
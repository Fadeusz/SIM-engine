
import base64
import os
from App.Connection import SendLine
from App.WebSocket import WebSocketClient_Send
import App.Config
class ToneDialing:

	Config = {}
	Progress = None

	def __init__(self):
		print("Init ToneDialing Class")

	def Configure(self, ob):
		self.Config = ob

	def Reset(self):
		print("Tone Dialing reset progress..")
		self.Progress = None

	def Run(self):
		#audio = self.Config["title_audio"]
		#self.Play(audio)

		self.Progress = self.Config
		self.Worker()
		
	def Play(self, e):
		b = base64.b64decode(e)
		f = open("Assets/Records/Tmp/tone.mp3", "wb")
		f.write(b)
		f.close()
		os.system("pkill ffplay")
		#os.system("omxplayer -o alsa Assets/Records/Tmp/tone.mp3")
		os.system("ffplay -nodisp -autoexit Assets/Records/Tmp/tone.mp3");

	def Click(self, tone):
		print("Tone:" + tone)

		#if self.Progress == None:
			#self.Progress = self.Config

		#print(self.Progress["options"])


		if tone in self.Progress["options"]:
			self.Progress = self.Progress["options"][tone]
			self.Worker()
		else:
			print("options not contains this tone")
		

	def Worker(self):

		print(self.Progress)

		self.Play(self.Progress["title_audio"])

		if "final_action" in self.Progress:
			if self.Progress["final_action"] == "end":
				self.EndConversation()
			elif self.Progress["final_action"] == "call":
				self.ConnectWithConsultant()


	def EndConversation(self):
		print(" ---- END ---- ")
		SendLine("ATH", False)

	def ConnectWithConsultant(self):
		print("Lączenie z konsultanem...")
		os.system("screen -dm ffplay -nodisp -autoexit -loop 0 Assets/Records/elevator.mp3");
		WebSocketClient_Send({"action":"ConsultantNeeded", "Current_Caller": App.Config.Current_Caller})

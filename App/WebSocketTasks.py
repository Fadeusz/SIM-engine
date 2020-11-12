import json
from App.SMS_Send import SMS_Send
import App.Config
import io
import App.WebSocket
import os
def WebSocketTasks(ob):
	print("Websocket TASK:")
	print(ob)
	if "action" in ob:

		if ob["action"] == "easy_sms":
			SMS_Send.add_to_queue(ob['number'], ob['text'])
		elif ob["action"] == "SaveToneDialing":
			t = ob['ob']
			print(t)
			f = open("Config/ToneDialing.json", "w+")
			f.write(t)
			f.close()
			try:
				App.Config.ToneDialing.Configure(json.load(io.StringIO(t)))
			except:
				print("Error - ToneDialing Configure")



		elif ob["action"] == "ConsultantReady":
			print("Consultant Ready!")
			print(App.Config.Current_Caller)
			if App.Config.Current_Caller != 0:
				print("Is the consultant still waiting to talk?")
				App.WebSocket.WebSocketClient_Send({"action":"ConnectWithConsultant", "Current_Caller": App.Config.Current_Caller})
			else:
				print("The conversation with the consultant will not take place")


		elif ob["action"] == "AudioStreamStart":
			print("Starting audio stream...")
			os.system("pkill ffplay")
			App.Config.Micro.run()

			
		else:
			print("Ordered unfamiliar action from a remote controller")

	else:
		print("No action from the remote controller is given")
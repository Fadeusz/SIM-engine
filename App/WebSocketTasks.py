import json
from App.SMS_Send import SMS_Send
import App.Config
import io
import App.WebSocket
import os
import base64
import time
import math
def WebSocketTasks(ob):
	print("Websocket TASK:")
	print(ob)
	if "action" in ob:

		if ob["action"] == "easy_sms" or ob["action"] == "mail_to_sms":
			SMS_Send.add_to_queue(ob['number'], ob['text'], ob["unique_id"])
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

		elif ob["action"] == "LastMessagesTimes":
			print("SQL Controller update!")
			sms_time = int(ob["sms"])
			mms_time = int(ob["mms"])

			sms_list = App.Config.SQL.select("SELECT number, msg, date, time FROM sms WHERE time > ?", (sms_time,))
			mms_list = App.Config.SQL.select("SELECT * FROM mms WHERE time > ?", (mms_time,))
			for o in mms_list:
				o = list(o)
				#response = reqs.post(App.Config.Controller.Address + "/ajax/MMSFromDevice", d)
				#print(response.text)

				if o[6] == "4":
					o[5] = o[5].encode('utf-8')
				
				file = base64.b64encode(o[5]).decode()

				n = 10000
				parts = math.ceil(len(file) / n)
				for i in range(0, len(file), n):
					#time.sleep(1)
					d = {
						"number": o[1],
						"date": o[2],
						"time": o[3],
						"unique_id": o[4],
						"file": file[i:i+n],
						"file_type": o[6],
						"file_name": o[7]
					}
					App.WebSocket.WebSocketClient_Send({"action":"MMS_Received", "ob": d, "part": int(i/n), "parts": parts})

			App.WebSocket.WebSocketClient_Send({"action":"UpdateSMSBase", "ob": sms_list})
			#App.WebSocket.WebSocketClient_Send({"action":"UpdateMMSBase", "ob": mms_list})

			
		else:
			print("Ordered unfamiliar action from a remote controller")

	else:
		print("No action from the remote controller is given")
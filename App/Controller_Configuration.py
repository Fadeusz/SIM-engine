import requests as reqs
import json
import hashlib
from io import StringIO
import time
import App.Config
from App.WebSocket import WebSocketClient_Run
class Controller_Configuration:
	Address = None
	Email = None
	Password = None

	response = None
	LoginData = None

	LastLoginTime = 0
	SuccessLogin = False

	def __init__ (self):

		f = open("Config/Controller_Login.txt", "r")
		c = f.read()
		lines =  c.split("\n")
		lines_c = len(lines)
		print("Controller init")
		print("Controller login file lines: " + str(lines_c) )

		if lines_c >= 3:
			self.Address = lines[0]
			self.Email = lines[1]
			self.Password = lines[2]
			
			if lines_c > 3 and lines[3] != "":
				App.Config.WebSocket["url"] = lines[3]

			if lines_c > 4 and lines[4] != "":
				App.Config.WebSocket["key"]  = lines[4]

	def SetNewData(self, address, email, password):
		self.Address = address
		self.Email = email

		result = hashlib.sha256(password.encode())
		self.Password = result.hexdigest()

	def Login(self):
		url = self.Address + "/ajax/ApplicationLogin"
		data = {'email': self.Email, 'password': self.Password, 'unique_id': App.Config.unique_id}
		response = reqs.post(url, data, allow_redirects=False)
		#print("response.headers['Location'] ->" + response.headers['Location'])
		print("response.status_code --> '"+str(response.status_code)+"'")
		if response.status_code == 301:
			response = reqs.post(response.headers['Location'], data, allow_redirects=False)

		self.response = response

		s = self.CheckLoginStatus()
		self.SuccessLogin = s

		if s == True: 
			self.LastLoginTime = time.time()
			self.SaveLoginToFile()
			self.SaveVariable()

			if "connected" in App.Config.WebSocket and App.Config.WebSocket["connected"] != 0:
				print("Socket is already running")
			else:
				WebSocketClient_Run()
				

		return str(s)

	def CheckLoginStatus(self):
		if self.response.status_code != 200: return False

		print("Controller Login Response Data:")
		print(self.response.text)

		io = StringIO(self.response.text)
		ob = json.load(io)
		self.LoginData = ob
		return ob["success"]

	def SaveLoginToFile(self):
		f = open("Config/Controller_Login.txt", "w+")
		f.write(self.Address + "\n")
		f.write(self.Email + "\n")
		f.write(self.Password)
		f.close()

	def SaveVariable(self):
		print("Socket URL:")
		print(self.LoginData["data"]["SocketEngine"])
		App.Config.WebSocket["url"] = self.LoginData["data"]["SocketEngine"]
		App.Config.WebSocket["key"] = self.LoginData["data"]["TempKey"]
		App.Config.WebSocket["pending"] = self.LoginData["data"]["pending"]

	def UpdateStatus(self):

		if "connected" in App.Config.WebSocket and App.Config.WebSocket["connected"] != 0:
			return "2"

		if time.time() - self.LastLoginTime > 10:
			self.Login()

		#Po zalogowaniu laczy z socketem jeszcze raz - sprobujmy jeszcze raz czy zmienilo status...
		if "connected" in App.Config.WebSocket and App.Config.WebSocket["connected"] != 0:
			return "2"

		if self.SuccessLogin == True:
			if App.Config.WebSocket["pending"] == True:
				return "12"
			else:
				return "1"
		else:
			return "0"


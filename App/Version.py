import requests

class Version:

	def __init__(self):
		self.GetFromFile()
		self.GetFromWebsite()
		self.Compare()

		print("Version is " + ("" if self.latest else "NOT ") + "up to date")

	def GetFromFile(self):
		with open('VERSION.txt') as f:
			self.current = f.readline().strip()
			#print("Version in file: " + self.current)

	def GetFromWebsite(self):
		response = requests.get("https://raw.githubusercontent.com/Fadeusz/SIM-engine/master/VERSION.txt")
		self.official = response.text.strip()
		#print("official version: " + self.official)

	def Compare(self):
		self.latest = (self.current == self.official)
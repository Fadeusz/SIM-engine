import uuid
from App.Connection import SendLine
import App.Config


class MMS_Received:
	def __init__(self, line):
		print("Creating MMS object.")
		l = line.split('"')
		self.number = l[1]
		self.date = l[3]
		self.unique = str(uuid.uuid4())

	def add_file(self, line):
		print("MMS LINE: " + line)
		l = line.split(",")
		file_type = l[2]
		file_name = l[1].replace('"', "")
		file_size = int(l[3])
		if file_name != "":
			print("Saving MMS image...")
			if file_type == "4":
				skip = [0]
			else:
				skip= []
			img = SendLine("AT+CMMSREAD=" + l[0], arrBytes=True, arrBytesLength=file_size, skipChars=skip)
			if file_type == "4":
				i = 0
				newString = ""
				arr = img
				while i < len(arr):
					if len(arr) > i + 1 and arr[i + 1] == 1:
						newString += chr(arr[i] + 256)
						i += 1
					else:
						newString += chr(arr[i])
					i += 1
				img = newString

			#newFile = open("Data/" + file_name, "wb")
			#newFile.write(img)
			App.Config.SQL.execute("INSERT INTO mms VALUES (null, ?, ?, ?, ?, ?, ?)", (self.number , self.date , self.unique , img , file_type , file_name))
			print("MMS saved.")


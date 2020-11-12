import base64
from io import BytesIO
f = open("fff.jpg", "rb")
data12 = f.read()
i = 0
for x in data12:
	print "--------------------------"
	i = i+1
	print str(i) + ": " + x + " ----> " + str(ord(x))
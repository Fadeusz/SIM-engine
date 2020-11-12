f = open("Assets/Images/fff.jpg", 'rb')
data12 = f.read()
#Write(data12.encode())

i = 0
for x in data12:
	print(chr(x))
	#print(len(x))
	i=i+1
	if i > 30:
		break
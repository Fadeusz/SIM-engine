import time

from App.Connection import SendLine, Write

class MMS_Send:
	@staticmethod
	def Send(number, att):
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
		time.sleep(1)
		SendLine('AT+SAPBR=1,1')
		time.sleep(1)
		SendLine("AT+CMMSEDIT=1")
		time.sleep(1)

		t = type(att).__name__
		if t == "str": att = [att]

		while att:
			f = open("Assets/Images/" + att.pop(0), "rb")
			data12 = f.read()
			SendLine('AT+CMMSDOWN="PIC",' + str(len(data12)) + ',307200,"LCI-'+str(int(time.time()))+'.jpg"') #307200 - max await time
			
			time.sleep(2)
			Write(data12, False)
			#for x in data12:
				#Write(chr(x))
				#Write(str(chr(x).encode('ascii', 'replace'))[2:-1])

			time.sleep(3)

		
		#SendLine('AT+CMMSDOWN="TITLE",3,5000')
		#ser.write("123")
		SendLine(u'AT+CMMSRECP="'+number+'"')
		time.sleep(1)
		SendLine('AT+CMMSSEND')
		time.sleep(1)
		SendLine("AT+CMMSVIEW", False)
		time.sleep(1)
		SendLine("AT+CMMSEDIT=0", False)
		time.sleep(1)
		SendLine("AT+CMMSVIEW", False)
		time.sleep(1)
		SendLine("AT+CMMSTERM", False)

	queue = []

	@staticmethod
	def add_to_queue(number, attach):
		MMS_Send.queue.append([number, attach])

	@staticmethod
	def send_first():
		ar = MMS_Send.queue.pop(0)
		MMS_Send.Send(ar[0], ar[1])
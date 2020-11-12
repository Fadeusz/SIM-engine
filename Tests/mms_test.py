# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import serial
import time,sys
import re
import binascii
import threading
import os

SERIAL_PORT = "/dev/ttyS0"

ser = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 0.5)


def SendLine(line):
	ser.write(line + "\r")



SendLine('AT+CMMSINIT')
time.sleep(2)
SendLine('AT+CMMSCURL="http://mms.orange.pl"')
time.sleep(2)
SendLine('AT+CMMSCID=1')
time.sleep(2)
SendLine('AT+CMMSPROTO="192.168.6.104",8080')
time.sleep(2)
SendLine('AT+CMMSSENDCFG=6,3,0,0,2,4')
time.sleep(2)
SendLine('AT+SAPBR=3,1,"Contype","GPRS"')
time.sleep(2)
SendLine('AT+SAPBR=3,1,"APN","internet"')
time.sleep(2)
SendLine('AT+SAPBR=1,1')
time.sleep(2)
SendLine('AT+SAPBR=2,1')


f = open("example-stamp-260nw-426673501.jpg", "rb")
img = f.read()
data = img.encode('hex')
data = " ".join([data[i:i+2] for i in range(0, len(data), 2)])
print str(len(img))

SendLine("AT+CMMSEDIT=1")
SendLine('AT+CMMSDOWN="PIC",' + str(len(img)) + ',20000')
time.sleep(5)
#SendLine("FE FF " + data)
SendLine(data)
time.sleep(5)
#time.sleep(20)
#SendLine('AT+CMMSDOWN="TITLE",3,5000')
#ser.write("123")
SendLine('AT+CMMSRECP="884167733"')
SendLine("AT+CMMSVIEW")
SendLine('AT+CMMSSEND')
SendLine("AT+CMMSEDIT=0")
SendLine("AT+CMMSTERM")

print ser.read()
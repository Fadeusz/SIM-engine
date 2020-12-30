import os
import datetime

def LogDirExist():
	if not os.path.exists('Logs'):
		os.makedirs('Logs')


def Serial(line):
	LogDirExist()

	log = "[" + datetime.datetime.now().strftime("%d.%b %Y %H:%M:%S") + "] " + line
	with open('Logs/Serial.txt', 'a') as file:
		file.write(log)

	l = 0
	with open('Logs/Serial.txt') as f:
		l = len(f.read())
	
	if l > 10000000:
		t = datetime.datetime.now().strftime("%d-%b-%Y>%H:%M:%S")
		os.rename(r'Logs/Serial.txt',r'Logs/Serial-' + t + '.txt')
# -*- coding: utf-8 -*-

print("Loading....")


import signal
import sys
import os

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    os._exit(0)
signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C if you can close program')

import App.Arguments
App.Arguments.Init()


from multiprocessing import Process
from threading import Thread

from App.Web import app

from App.WebSocket import WebSocketClient_Run, WebSocketClient_Stop, WebSocketClient_Send

import App.Config

from App.Version import Version
App.Config.Version = Version()

#App.Config.WebSocket = {"url":"ws://srv01.letscode.it:8031/"}

#WSLoop = Process(target=WebSocketClient_Run)
#WSLoop.start()
#WS.Send("TESTOWE")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def webStart():
	try:
		app.run(debug=False, host='0.0.0.0', port=App.Arguments.args.webport)
	except:
		print(bcolors.FAIL + "WebServer problem, on port: " + str(App.Arguments.args.webport))
		os._exit(0)

wstart = Thread(target=webStart)
wstart.start()




from App.SQL import SQL
App.Config.SQL = SQL()

from App.Init import Init

I = Init()

if I.res == True:

    App.Config.LoadingApplication = False

    from App.loop import Loop
    SerialLoop = Thread(target=Loop)
    SerialLoop.start()

    from App.Microphone import micro
    App.Config.Micro = micro()

else:
    App.Config.ATInitProblem = True
    print("Go to:")
    print("        http://192.168.1.18:8025/system_configuration")

#WebSocketClient_Send("testowe xd")

#if __name__ == '__main__':
	#app.run(debug=False, host='0.0.0.0', port=8025)
# -*- coding: utf-8 -*-

print("Loading....")

from multiprocessing import Process
from threading import Thread

from App.Web import app

from App.WebSocket import WebSocketClient_Run, WebSocketClient_Stop, WebSocketClient_Send

import App.Config

#App.Config.WebSocket = {"url":"ws://srv01.letscode.it:8031/"}

#WSLoop = Process(target=WebSocketClient_Run)
#WSLoop.start()
#WS.Send("TESTOWE")

from App.Init import Init

I = Init()

from App.loop import Loop
SerialLoop = Thread(target=Loop)
SerialLoop.start()


from App.Microphone import micro
App.Config.Micro = micro()


#WebSocketClient_Send("testowe xd")

if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0', port=8025)
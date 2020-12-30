import websocket

import json
from io import StringIO, BytesIO

#try:
#    import thread
#except ImportError:
#    import _thread as thread

from time import sleep

import App.Config

from threading import Thread

from App.WebSocketTasks import WebSocketTasks

ws = None

import struct

from pygame import mixer, time

def on_message(ws, message):
    #print(message)
    
    thisIsJSON = False

    try:
        io = StringIO(message)
        ob = json.load(io)
        thisIsJSON = True
        print("This is json!")
    except:
        print("Dane nie są jsonem")

    if thisIsJSON == True:
        try:
            WebSocketTasks(ob)
        except Exception as e: print(e)
    else:
        #a = struct.unpack('4096h', message[44:])
        if len(message) == 8236:
            try:
                mixer.pre_init(44100, -16, 1, 4096)
                mixer.init()
                sound = mixer.Sound(buffer=message[44:])
                audio = sound.play()
            except:
                print("Wrong binary data from controller ")

        else:
            print("To nie json!")

def on_error(ws, error):
    App.Config.WebSocket["connected"] = 0
    print(error)

def on_close(ws):
    print("### closed ###")

    sleep(15)
    ws.keep_running = False
    App.Config.Controller.UpdateStatus()
    #if App.Config.WebSocket["connected"] == 0:
        #WebSocketClient_Run()

def on_open(ws):
    App.Config.WebSocket["connected"] = 1

def on_run():
    print("Init web socket")
    #websocket.enableTrace(True)
    global ws
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(App.Config.WebSocket["url"] +  '?type=device&key=' + App.Config.WebSocket["key"] + '&id=' + App.Config.unique_id,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

def WebSocketClient_Run():
    #thread.start_new_thread(on_run, ())
    #on_run()
    global ws
    if ws != None:
        ws.keep_running = False

    if "url" in App.Config.WebSocket:
        global WSLoop
        WSLoop = Thread(target=on_run)
        WSLoop.start()
    else:
        print("Socket URL not defined.")

def WebSocketClient_Stop():
    ws.keep_running = False

def WebSocketClient_Send(txt):

    try:
        s = json.dumps(txt)
        ws.send(s)
        #print("SEND -> " + s)
    except: 
        print("I can only send json")

def WebSocketClient_SendBinary(txt):
    ws.send(txt, 0x2)

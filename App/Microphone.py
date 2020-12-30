import pyaudio

from App.WebSocket import WebSocketClient_SendBinary
import App.Config

from threading import Thread

class micro:

	stopped = False

	def loop(self):

		CHUNK = 4096
		FORMAT = pyaudio.paInt16
		CHANNELS = 1
		RATE = 44100

		print("Mic listen....")

		p = pyaudio.PyAudio()

		stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

		while self.stopped == False:
			try:
				data = stream.read(CHUNK)
				#print(len(data))
				#WebSocketClient_Send( base64.b64encode( data) )
				WebSocketClient_SendBinary(data)
			except:
				print("Except in stream read")

		print("Audio stream stopped.")

		stream.stop_stream()
		stream.close()
		p.terminate()

	def __init__ (self):
		print("mic loaded")

	def run(self):
		self.stopped = False
		self.MicReader = Thread(target=self.loop)
		self.MicReader.start()

	def stop(self):
		self.stopped = True
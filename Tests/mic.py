import pyaudio

CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

while 1:
    data = stream.read(CHUNK)
    print(len(data))

stream.stop_stream()
stream.close()
p.terminate()
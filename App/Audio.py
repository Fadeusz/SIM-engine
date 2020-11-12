import os

def play(s):
	os.system("pkill omxplayer")
	return os.system("omxplayer -o alsa Assets/Records/" + s + ".mp3")
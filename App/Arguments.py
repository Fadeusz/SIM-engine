import argparse

args = {}

def Init():
	global args
	parser = argparse.ArgumentParser()
	parser.add_argument('--webport', help='Port from WebServer (default 8025)', default=8025, type=int)
	parser.add_argument('--showcontroller', help='Enter true if you want to be able to change the default controller address', default=False, type=bool)
	args = parser.parse_args()
import argparse

args = {}

def Init():
	global args
	parser = argparse.ArgumentParser()
	parser.add_argument('--webport', help='Port from WebServer (default 8025)', default=8025, type=int)
	args = parser.parse_args()
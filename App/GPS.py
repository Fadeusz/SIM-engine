from App.SMS_Send import SMS_Send

class GPS:
	@staticmethod
	def get_position(line):
		args = line.split(",")
		return args[3] + "," + args[4]

	awaiting_location_list = []

	@staticmethod
	def do_list(line):
		position =  GPS.get_position(line)
		if position != ",":
			msg = "https://www.google.com/maps/place/" + position
		else:
			msg = "Location Not Avaiable"

		while len(GPS.awaiting_location_list) > 0:
			nr = GPS.awaiting_location_list.pop(0)
			SMS_Send.add_to_queue(nr, msg)
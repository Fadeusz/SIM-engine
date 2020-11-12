import binascii

class UTF16:
	def encode(text):
		return str(binascii.hexlify(text.encode('utf-16-be')))[2:-1]

	def decode(text):
		return binascii.unhexlify(text).decode('utf-16-be')
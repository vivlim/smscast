class LibSMSCast:
	def __init__(self):
		pass
	def send(self, to, msg):
		for recipient in to:
			print("\"{}\" -> {}".format(msg, recipient))
			

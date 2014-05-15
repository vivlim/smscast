class LibSMSCast:
	def __init__(self):
		pass
	def send(self, to, msg):
		f = open('mocksms.log', 'a')
		for recipient in to:
			f.write("\"{}\" -> {}\n".format(msg, recipient))
		f.close()

			

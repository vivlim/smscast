
import config
from twilio.rest import TwilioRestClient

class LibSMSCast:

	def __init__(self):
		self.client = TwilioRestClient(config.ACCOUNT_SID, config.AUTH_TOKEN)

	def send(self, to, msg):
		for recipient in to:
			self.client.messages.create(
					to=recipient,
					from_=config.FROM_NUMBER,
					body=msg,
					)



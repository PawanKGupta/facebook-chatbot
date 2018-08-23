from wit import Wit

access_token = "FYI337FF7KHF4YOSPIP35D4TTPJZBMFS"

client = Wit(access_token = access_token)

def get_resp(message_text):
	resp = client.message(message_text)
	entity = None
	value = None

	try:
		entity = list(resp['entities'])[0]
		value = resp['entities'][entity][0]['value']
	except:
		pass

	return (entity, value)
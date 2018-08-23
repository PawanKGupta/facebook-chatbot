import os, sys
from flask import Flask, request
from pymessenger import Bot

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAH3Y98xri4BAIFQuaUFDfKEp8DN8WJ9k6GzoRMhKI5thpk8gUszJTygzoy3DdxWGfuThp7sLJCGUrFihrY6ObxDcwiKjNI65sW0HVlIaSemS80rCV7cJ29wvSrPuuAT67ZCNQsCBIhFMUKSh4UrdZBoZC5XDa8GSI7ZBrLaZAc72uI8ZBZA4qn"

bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/webhook', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/webhook', methods=['POST'])
def webhook():
	data = request.get_json()
	log(data)

	if data['object'] == 'page':
		for entry in data['entry']:
			for messaging_event in entry['messaging']:

				# IDs
				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']

				if messaging_event.get('message'):
					# Extracting text message
					if 'text' in messaging_event['message']:
						messaging_text = messaging_event['message']['text']
					else:
						messaging_text = 'no text'

					# Echo
					response = messaging_text
					#response = "I'm able to hear you!!"
					bot.send_text_message(sender_id, response)

	return "ok", 200


def log(message):
	print(message)
	sys.stdout.flush()


if __name__ == "__main__":
	app.run(debug = True)
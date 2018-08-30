import os, sys
from threading import Thread

from flask import Flask, request
from pymessenger import Bot

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAH3Y98xri4BAHBb2NvwVBsZA3Q0hxyHp0CbNVf0q93XWvdktsVPtJDugqMG9PKfXlz3i9Qf0jakNqqgwIZB8zAzXKaTfow18W5uFUFwML7y1b52EoSUJwMbnFt1vQprEumTNN5kDBfMZBkS4JaWUY3pjb8jhlj9aZCmIBqAtpIpyvUOZCiwl"

bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/', methods=['GET'])
def verify():
    # Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
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
                        print(
                            "*********************************************************************************" + messaging_text)
                    else:
                        messaging_text = 'no text'
                    response = messaging_text
                    bot.send_text_message(sender_id, response)
        # return messaging_text
        return "ok", 200


def log(message):
    print(message)
    sys.stdout.flush()


def run_main():
    app.run(debug=True)
    #child_thread.start()


# if __name__ == "__main__":
#     # messaging_text = app.run(debug=True)
#
#     child_thread = Thread(target=run_main())
#     child_thread.start()
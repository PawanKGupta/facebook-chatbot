import os, sys
from flask import Flask, request
#from pymessenger import Bot

app = Flask(__name__)

#PAGE_ACCESS_TOKEN = "EAAH3Y98xri4BAEZBuAxmNicDuLYADjyp6c5yNieovQCtZAbYfE10x7azydhxOlzRM3o4C9z2VG60tPLi90wF2WBCBZAdtkqJ5bfq9bRy6ztgeWrHziCM3cynWLS7jSsqv0XzVrlERNEikPXrtejdebHw58uCcz4JSNWoZA1v1yT75HFLRoe6"

#bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/webhook', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello world":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200



if __name__ == "__main__":
	app.run(debug = True, port = 80)
import json
import  sys
import re
from threading import Thread

import traceback

from flask import Flask, request
from pymessenger import Bot

from viewRequest import view_request

sys.path.append("..")
from Framework.dialogflowConn import apiaiCon

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAH3Y98xri4BAOOp1UlkLxQl31cL7A8ZATN0gec84jRiayWsWdlACVguhrzhgVd86ZBlnvRqo2ytCf996OFqfE4gSCgBZApAvW5JLhl3V8QSt0pdBcpXERbHZBk0O9HuA55CDNgWdwNZAUC4GlWDvhbhftIZAZAL9phmyZA4rqJAW2wbMH2YluNt"

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


                    if messaging_text.__contains__("request id") == True or messaging_text.isdigit() == True:
                        if messaging_text.__contains__("request id") == True:
                            req_id = re.findall('\d+', messaging_text)[0]
                        else:
                            req_id = messaging_text
                        reply = view_request(req_id)
                    else:
                        reply = apiaiCon(messaging_text)
                    details = read_jsondata()
                    if (messaging_text.lower()).__contains__("status") == True:
                        reply = "Status of your request is now {}.".format(details['requestInfo']['status'])
                    if (messaging_text.lower()).__contains__("subject") == True:
                        if details.__contains__("subject"):
                            reply = "Subject of your request is: {}.".format(details['requestInfo']['subject'])
                        else:
                            reply = "there is no sbject available for this request."
                    if (messaging_text.lower()).__contains__("technician") == True:
                        reply = "Assigned technician is {}.".format(details['requestInfo']['technician'])
                    if (messaging_text.lower()).__contains__("item") == True:
                        reply = "This request is for {} item.".format(details['requestInfo']['item'])
                    if (messaging_text.lower()).__contains__("created") == True and (
                            messaging_text.lower()).__contains__("date") == True:
                        reply = "This request created at Date: {}".format(details['requestInfo']['createdDate'])
                    if (messaging_text.lower()).__contains__("item") == True and (messaging_text.lower()).__contains__(
                            "type") == True:
                        reply = "Item type is: {}.".format(details['requestInfo']['itemType'])

                    bot.send_text_message(sender_id, reply)
        # return messaging_text
        return "ok", 200

def read_jsondata():
    """
    This function store the REST data in txt format at provided location path
    Arguments: rest_data
    Returns: NA
    """
    try:
        path = "D:\\facebookBot\\facebook_chatbot\\temp"
        file = open(path + "\\request_details.json", "r+")
        data = json.load(file)
        file.close()
        return data
    except Exception as ex:
        # print("exception" + ex.message)
        print(traceback.format_exc())
        return 1

def log(message):
    print(message)
    sys.stdout.flush()


def run_main():
    app.run(debug=True)


if __name__ == "__main__":
    # messaging_text = app.run(debug=True)

    child_thread = Thread(target=run_main())
    child_thread.start()

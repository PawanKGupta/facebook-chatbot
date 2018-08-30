import json
import os, sys
import re
from threading import Thread

import traceback

from flask import Flask, request
from pymessenger import Bot

sys.path.append("..")
from Framework.utils import get_resp
import getRequestDetail

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAH3Y98xri4BAPuYyRr9tt75Ybze0gcurypOAakKqUfKZCZAjylQJD7v5dz4zdQ8gy9YybrY9bCKdTmhg3FUtolJvIaYnisCC1uPxLgFo0qplFmodd0HGgAxH1ZCtej5VH613OMUBUM0xxvyM2vcZAlgYl9jMUmDcYS4H3cF8fZCSE24deMXs"

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
                        response = view_request(req_id)
                    else:
                        response = reply(messaging_text)
                    details = read_jsondata()
                    if (messaging_text.lower()).__contains__("status") == True:
                        response = "Status of your request is now {}.".format(details['requestInfo']['status'])
                    if (messaging_text.lower()).__contains__("subject") == True:
                        if details.__contains__("subject"):
                            response = "Subject of your request is: {}.".format(details['requestInfo']['subject'])
                        else:
                            response = "there is no sbject available for this request."
                    if (messaging_text.lower()).__contains__("technician") == True:
                        response = "Assigned technician is {}.".format(details['requestInfo']['technician'])
                    if (messaging_text.lower()).__contains__("item") == True:
                        response = "This request is for {} item.".format(details['requestInfo']['item'])
                    if (messaging_text.lower()).__contains__("created") == True and (
                            messaging_text.lower()).__contains__("date") == True:
                        response = "This request created at Date: {}".format(details['requestInfo']['createdDate'])
                    if (messaging_text.lower()).__contains__("item") == True and (messaging_text.lower()).__contains__(
                            "type") == True:
                        response = "Item type is: {}.".format(details['requestInfo']['itemType'])
                    # if messaging_text == "yes":
                    #      response = "I got you"

                    bot.send_text_message(sender_id, response)
        # return messaging_text
        return "ok", 200


def reply(messaging_text):
    # print(messaging_text)
    entity, value = get_resp(messaging_text)
    if entity == "greetings":
        response = "Hello! Welcome to ZENWorks Service Desk. How can i help you?"
    elif entity == "problem":
        response = "Cool! which type of {} is this?".format(value)
    elif entity == "view_request":
        response = "Please give your Ticket ID."
    elif entity == "create_request":
        response = "I can {} but now i am learning how to create request.".format(value)
    elif entity == "thanks":
        response = "Thanks for contacting ZENworks Service Desk chatbot. We always happy to help you. bye bye :)"
    elif entity == "personal":
        response = "I'm good. how are you?"
    else:
        response = "Sorry! I didn't get you."
    return response


def view_request(req_id):
    details = getRequestDetail.getRequestDetail().getRequest(req_id)
    if details == "No Request":
        response = "Your request does not exist in Database. Please give a valid id!!"
    elif details == None:
        response = "Sorry! service desk server is not able to authenticate you."
    else:
        # status = details['requestInfo']['status']
        response = "which information you want about your request?"
    # print("************************" + str(details))
    store_jsondata(details)
    return response


def store_jsondata(details):
    """
    This function store the REST data in txt format at provided location path
    Arguments: rest_data
    Returns: NA
    """
    try:
        path = "D:\\facebookBot\\facebook_chatbot\\temp"
        if not os.path.exists(path):
            os.makedirs(path)
        extension = '.json'
        file = open(path + "\\request_details" + extension, "w+")
        json.dump(details, file)
        # file.write(details)
        file.close()
    except Exception as ex:
        # print("exception" + ex.message)
        print(traceback.format_exc())
        return 1


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

# def create_request():
#     app2.run_main()


if __name__ == "__main__":
    # messaging_text = app.run(debug=True)

    child_thread = Thread(target=run_main())
    child_thread.start()

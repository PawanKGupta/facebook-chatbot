import json
import sys
import re
from threading import Thread

import traceback

from flask import Flask, request
from pymessenger import Bot

from Framework.storeJSONData import store_jsondata
from viewRequest import view_request
from createRequest import createRequest

sys.path.append("..")
from Framework.dialogflowConn import apiaiCon

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAJwcL5QwhMBAPTicqHElt13oCbS7DSDXqOGDz4VlZBZBfYlu66jeb77zh2XHZBFCbuFmFHFjB4ZCJk29TZCnAp47LpIUxJMuB3xuFwg7iwedkaBrTzZCp4jojiO1F8ZAOZCOxaVQ1XfbuzYAOUde6vhLZBe3Kt3AhjPZBvRSLx9Bl5jfdBKvxZAzUEZBLXYlOzpK28ZD"

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
                    action = "None"
                    resolvedQuery = "None"
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                        print(
                            "*********************************************************************************" + messaging_text)
                    else:
                        messaging_text = 'no text'


                    # if messaging_text.__contains__("request id") == True or messaging_text.isdigit() == True:
                    #     if messaging_text.__contains__("request id") == True:
                    #         req_id = re.findall('\d+', messaging_text)[0]
                    #     else:
                    #         req_id = messaging_text
                    #     reply = view_request(req_id)
                    # else:
                    #     reply, action, resolvedQuery = apiaiCon(messaging_text)
                    reply, action, resolvedQuery = apiaiCon(messaging_text)
                    if (action == "return-request-id"):
                        req_id = messaging_text
                        reply = view_request(req_id)
                    if (action == "smalltalk.appraisal.thank_you"):
                        details = {"requestAdditionalInfo": {"contactTime": "No Data"}, "requestCustomFieldInfo": [], "requestInfo": {"canApprove": "No Data", "category": "No Data", "classification": "No Data", "closedDate": "No Data", "createdDate": "No Data", "description": "No Data", "hasAttachment": "No Data", "item": "No Data", "itemType": "No Data", "priority": "No Data", "requestNumber": 100086, "requestType": "No Data", "requestor": "No Data", "room": "No Data", "status": "No Data", "subject": "No Data", "technician": "No Data", "urgency": "No Data"}, "requestNotes": []}
                        store_jsondata(details)
                    if (action == "CreateRequest.CreateRequest-yes" and resolvedQuery.lower() == "yes") or (action == "BasicQuestion.BasicQuestion-yes" and resolvedQuery.lower() == "yes"):
                        req_id = createRequest.create_request("test")
                        #req_id = "987654"
                        reply = "Your request has been raised successfully. This is your request_id : "+str(req_id)
                    elif reply.__contains__("Please describe your") == True:
                        bot.send_text_message(sender_id, reply)
                        reply = "As of now we havn't implemented knowledge base. Do you want to raise a ticket?"
                    details = read_jsondata()
                    if (messaging_text.lower()).__contains__("status") == True:
                        status = details['requestInfo']['status']
                        if status == "No Data":
                            reply = "No data found. Please give your Request_id."
                        else:
                            reply = "Status of your request is:  {}.".format(status)
                    if (messaging_text.lower()).__contains__("subject") == True:
                        if details.__contains__("subject"):
                            subject = details['requestInfo']['subject']
                            if subject == "No Data":
                                reply = "No data found. Please give your Request_id."
                            else:
                                reply = "Subject of your request is:  {}.".format(subject)
                        else:
                            reply = "there is no sbject available for this request."
                    if (messaging_text.lower()).__contains__("technician") == True:
                        technician = details['requestInfo']['technician']
                        if technician == "No Data":
                            reply = "No data found. Please give your Request_id."
                        else:
                            reply = "Assigned Technician is:  {}.".format(technician)
                    if (messaging_text.lower()).__contains__("item") == True:
                        item = details['requestInfo']['item']
                        if item == "No Data":
                            reply = "No data found. Please give your Request_id."
                        else:
                            reply = "This request is for item:  {}".format(item)
                    if (messaging_text.lower()).__contains__("created") == True and (
                            messaging_text.lower()).__contains__("date") == True:
                        createdDate = details['requestInfo']['createdDate']
                        if createdDate == "No Data":
                            reply = "No data found. Please give your Request_id."
                        else:
                            reply = "This request created at Date:  {}".format(createdDate)
                    if (messaging_text.lower()).__contains__("item") == True and (messaging_text.lower()).__contains__(
                            "type") == True:
                        itemType = details['requestInfo']['itemType']
                        if itemType == "No data":
                            reply = "No data found. Please give your Request_id."
                        else:
                            reply = "Item type is: {}.".format(itemType)

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

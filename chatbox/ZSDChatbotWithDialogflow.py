import json
import sys
import socket
import traceback

from Framework.storeJSONData import store_jsondata
from viewRequest import view_request
from CreateRequest import CreateRequest

sys.path.append("..")
from Framework.dialogflowConn import apiai_con


def webhook():
    s = socket.socket()
    host = socket.gethostname()
    print(" server will start on host : ", host)
    port = 8080
    s.bind((host, port))
    print("")
    print(" Server done binding to host and port successfully")
    print("")
    print("Server is waiting for incoming connections")
    print("")
    s.listen(1)
    conn, add = s.accept()
    print(add, " Has connected to the server and is now online ...")
    print("")
    while 1:
        messaging_text = conn.recv(1024)
        messaging_text = messaging_text.decode()
        print(" Client : ", messaging_text)

        reply, action, resolved_query = apiai_con(messaging_text)
        if action == "return-request-id":
            req_id = messaging_text
            reply = view_request(req_id)
        if action == "smalltalk.appraisal.thank_you":
            details = {"requestAdditionalInfo": {"contactTime": None}, "requestCustomFieldInfo": [],
                       "requestInfo": {"canApprove": None, "category": None, "classification": None,
                                       "closedDate": None, "createdDate": None, "description": None,
                                       "hasAttachment": None, "item": None, "itemType": None,
                                       "priority": None, "requestNumber": 100086, "requestType": None,
                                       "requestor": None, "room": None, "status": None,
                                       "subject": None, "technician": None, "urgency": None},
                       "requestNotes": []}
            store_jsondata(details)
        if action == "BasicQuestion.BasicQuestion-yes":
            req_id = CreateRequest.create_request(reply)
            if req_id is not None:
                reply = "Your request has been raised successfully. This is your request_id : " + str(req_id)
            else:
                reply = "Sorry! something went wrong during request creation. Please contact Administrator."
        # elif reply.__contains__("Please describe your"):
        #     reply = reply.encode()
        #     conn.send(reply)
        #     reply = "As of now we havn't implemented knowledge base. Do you want to raise a ticket?"
        details = read_jsondata()
        if (messaging_text.lower()).__contains__("status"):
            status = details['requestInfo']['status']
            if status == None:
                reply = "No data found. Please give your Request_id."
            else:
                reply = "Status of your request is:  {}.".format(status)
        if (messaging_text.lower()).__contains__("subject"):
            if details.__contains__("subject"):
                subject = details['requestInfo']['subject']
                if subject == None:
                    reply = "No data found. Please give your Request_id."
                else:
                    reply = "Subject of your request is:  {}.".format(subject)
            else:
                reply = "there is no subject available for this request."
        if (messaging_text.lower()).__contains__("technician"):
            technician = details['requestInfo']['technician']
            if technician == None:
                reply = "No data found. Please give your Request_id."
            else:
                reply = "Assigned Technician is:  {}.".format(technician)
        if (messaging_text.lower()).__contains__("item"):
            item = details['requestInfo']['item']
            if item == None:
                reply = "No data found. Please give your Request_id."
            else:
                reply = "This request is for item:  {}".format(item)
        if (messaging_text.lower()).__contains__("description"):
            description = details['requestInfo']['description']
            if description == None:
                reply = "No data found. Please give your Request_id."
            else:
                reply = "Description of the request is:  {}".format(description)
        if (messaging_text.lower()).__contains__("created") == True and (
                messaging_text.lower()).__contains__("date") == True:
            createdDate = details['requestInfo']['createdDate']
            if createdDate == None:
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
        reply = reply.encode()
        conn.send(reply)
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


if __name__ == "__main__":
    webhook()

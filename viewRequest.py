import json
import os
import traceback

import getRequestDetail


def view_request(req_id):
    details = getRequestDetail.getRequestDetail().getRequest(req_id)
    if details == "No Request":
        response = "Your request does not exist in Database. Please give a valid id!!"
    elif details == None:
        response = "Sorry! service desk server is not able to authenticate you."
    else:
        # status = details['requestInfo']['status']
        response = "which information do you want about your request?"
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

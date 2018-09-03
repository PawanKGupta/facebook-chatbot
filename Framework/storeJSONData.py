import json
import os
import traceback


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
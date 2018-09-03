import getRequestDetail
from Framework.storeJSONData import store_jsondata


def view_request(req_id):
    details = getRequestDetail.getRequestDetail().getRequest(req_id)
    if details == "No Request":
        response = "Your request does not exist in Database. Please give a valid id!!"
    elif details == None:
        response = "Sorry! service desk server is not able to authenticate you."
    else:
        # status = details['requestInfo']['status']
        response = "Thank you for giving request_id. What information do you want for your request?"
    # print("************************" + str(details))
    store_jsondata(details)
    return response




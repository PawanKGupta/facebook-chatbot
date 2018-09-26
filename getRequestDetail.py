import json
import traceback
import sys

sys.path.append('..')
from Framework.RestFactory import RestFactory
from Login.Login import Login
import logging

logging.basicConfig(level=logging.DEBUG)


class getRequestDetail:

    def getRequest(self, request_id):
        sd_ip = "10.71.64.192"
        try:

            print(sd_ip)
            token = Login.login(sd_ip)
            logging.debug(token)
            if token is not None:
                header = {"Authorization": "Berear " + token}
                url = "https://" + sd_ip + "/LiveTime/services/v1/customer/requests/{}".format(request_id)

                rest_data, rest_status = RestFactory().make_get_request(url, header)
                logging.debug(rest_status)
                if rest_status == 200:
                    jsonResponse = json.loads(rest_data.decode('utf-8'))
                else:
                    jsonResponse = "No Request"
                logging.debug(jsonResponse)
            else:
                jsonResponse = None
            return jsonResponse
        except Exception as ex:
            print(traceback.format_exc())
            return None
# getRequestDetail.getRequest(self=getRequestDetail)

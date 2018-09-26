import json
import traceback
import sys

from Login.Login import Login

sys.path.append("..")
from Framework.RestFactory import RestFactory
import logging

logging.basicConfig(level=logging.DEBUG)


class CreateRequest:
    def create_request(self, description):
        try:
            sd_ip = "10.71.64.192"
            req_id = None
            token = Login.login(sd_ip)
            logging.debug(token)
            if token != None:
                header = {"Authorization": "Berear " + token, "Content-Type": "application/json"}
                post_body_data = '{"requestDescription":'+'"'+description+'"'+', "subject":"Item category: Service and Item Type: Service Desk"}'
                url = "https://" + sd_ip + "/LiveTime/services/v1/customer/requests"
                rest_data, rest_status = RestFactory().make_post_request(url, post_body_data, header)
                logging.debug(rest_status)
                if rest_status == 200:
                    req_id = json.loads(rest_data.decode('utf-8'))
            logging.debug(req_id)
            return req_id
        except Exception as ex:
            print(traceback.format_exc())
            return None

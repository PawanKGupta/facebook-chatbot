import json
import traceback
import sys

sys.path.append("..")
from Framework.RestFactory import RestFactory
import logging

logging.basicConfig(level=logging.DEBUG)


class Login:
    def login(srever_ip):
        try:
            sd_ip = srever_ip
            header = {"Content-Type": "application/json"}
            post_body_data = '{"username":"nsdcustomer1", "password":"novell@123", "ldapSourceId":"1"}'
            url = "https://" + sd_ip + "/LiveTime/services/v1/auth/login"

            rest_data, rest_status = RestFactory().make_post_request(url, post_body_data, header)
            logging.debug(rest_status)
            token = None
            if rest_status == 200:
                jsonResponse = json.loads(rest_data.decode('utf-8'))
                for item, value in jsonResponse.items():
                    if item == "token":
                        token = value
            logging.debug(token)
            return token
        except Exception as ex:
            print(traceback.format_exc())
            return None

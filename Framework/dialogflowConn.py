import json

import apiai


# Connect to dialogflow
def apiaiCon(messaging_text):
    CLIENT_ACCESS_TOKEN = "887f7b06cc5f47f98357720ca306fb2a"
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'de'  # Default : English
    request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"
    request.query = messaging_text
    response = request.getresponse()
    obj = json.loads(response.read().decode())
    print(obj)
    reply = obj['result']['fulfillment']['speech']
    return reply

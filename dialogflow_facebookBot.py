from fbchat import Client, log
from fbchat.models import *
import apiai, codecs, json


class Jarvis(Client):

    # Connect to dialogflow
    def apiaiCon(self):
        self.CLIENT_ACCESS_TOKEN = "887f7b06cc5f47f98357720ca306fb2a"
        self.ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN)
        self.request = self.ai.text_request()
        self.request.lang = 'de'  # Default : English
        self.request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

    def onMessage(self, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        # Mark message as read
        self.markAsRead(author_id)

        # Print info on console
        log.info("Message {} from {} in {}".format(message_object, thread_id, thread_type))

        # Establish conn
        self.apiaiCon()

        # Message Text
        msgText = message_object.text

        # Request query/reply for the msg received
        self.request.query = msgText

        # Get the response which is a json object
        response = self.request.getresponse()
        obj = json.loads(response.read().decode())
        print(obj)

        # Get reply from the list
        reply = obj['result']['fulfillment']['speech']

        # Send message
        if author_id != self.uid:
            self.send(Message(text=reply), thread_id=thread_id, thread_type=thread_type)

        # Mark message as delivered
        self.markAsDelivered(author_id, thread_id)


# Create an object of our class, enter your email and password for facebook.
client = Jarvis("mr.pawan41@gmail.com", "Ilvbulbul48@")

# Listen for new message
client.listen()
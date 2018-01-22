from slackclient import SlackClient
import os
import responses as resp

# Template class to be inherited by future interface extensions
class Client:

    def __init__(self):
        self.interface = 'template'

    def connect(self):
        pass

    def get_bot_id(self):
        pass

    def read_message(self):
        pass

    def post_message(self, method, channel, response):
        pass

class Slack_Client(Client):

    def __init__(self):
        self.interface = "slack"
        self.client = SlackClient(os.environ.get('SLACK_TRAINING_BOT_TOKEN'))

    def connect(self):
        return self.client.rtm_connect(with_team_state=False)

    def get_bot_id(self):
        return self.client.api_call("auth.test")["user_id"]

    def read_message(self):
        return self.client.rtm_read()

    def post_message(self, method, channel, response):
        return self.client.api_call(method, channel=channel, text=response or resp.DEFAULT)

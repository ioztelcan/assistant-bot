import time
import re
import commands as cmd
import responses as resp
import client
import bot_lib as lib

# Instantiate Slack Client
bot_client = client.Slack_Client()

# Training bot ID, will be assigned later.
bot_id = None

# Constants
RTM_READ_DELAY = 1 # 1 sec delay between reading from RTM
MENTION_REGEX = "^<@(|[WU].+)>(.*)"

def parse_direct_mention(message):

    matches = re.search(MENTION_REGEX, message)
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def parse_commands(slack_events):

    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == bot_id:
                return message, event["channel"]

    return None, None

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith(cmd.HELP):
        response = resp.HELP
    elif command == cmd.PIRATE:
        response = resp.PIRATE
    elif command == cmd.MARKDOWN_SAMPLE:
        response = resp.MARKDOWN_SAMPLE
    elif command == cmd.BITCOIN_ACTUAL_PRICE:
        response = lib.get_bitcoin_price()

    # Sends the response back to the channel
    bot_client.post_message("chat.postMessage", channel, response)

if __name__ == "__main__":
    if bot_client.connect():
        print("Bot connected and active...")
        print("Interface: " + bot_client.interface)

        # Read bot's user ID by calling Web API method `auth.test`
        bot_id = bot_client.get_bot_id()

        while True:
            command, channel = parse_commands(bot_client.read_message())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed.")
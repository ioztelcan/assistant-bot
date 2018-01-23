import time
import re
import commands as cmd
import responses as resp
import client
import bot_lib as lib

# Instantiate client as a Slack Client
bot_client = client.Slack_Client()

# Bot ID in the chat application, will be assigned later.
bot_id = None

# Constants
READ_INTERVAL = 1 # 1 sec delay between reading from the interface.
MENTION_REGEX = "^<@(|[WU].+)>(.*)"

def parse_mention(message):

    matches = re.search(MENTION_REGEX, message)
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def parse_commands(events):

    for event in events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_mention(event["text"])
            if user_id == bot_id:
                return message, event["channel"]
            
    return None, None

def handle_command(command, channel):
    
    response = None
    if command.startswith(cmd.HELP):
        response = resp.HELP
    elif command == cmd.PIRATE:
        response = resp.PIRATE
    elif command == cmd.MARKDOWN_SAMPLE:
        response = resp.MARKDOWN_SAMPLE
    elif command == cmd.BITCOIN_ACTUAL_PRICE:
        response = lib.get_bitcoin_price()

    bot_client.post_message("chat.postMessage", channel, response)

if __name__ == "__main__":
    if bot_client.connect():
        print("Bot connected and active...")
        print("Interface: " + bot_client.interface)

        bot_id = bot_client.get_bot_id()

        while True:
            command, channel = parse_commands(bot_client.read_message())
            
            if command:
                handle_command(command, channel)
            time.sleep(READ_INTERVAL)
    else:
        print("Connection failed.")

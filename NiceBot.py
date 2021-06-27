import socket
from twitchbot import TwitchBot
from twitchbot.settings import BOT_USERNAME, CLIENT_ID, CLIENT_SECRET, TOKEN


def main():
    bot = TwitchBot()
    bot.connect()


if __name__ == "__main__":
    main()
from twitchbot import Twitch
from twitchbot.settings import BOT_USERNAME, CLIENT_ID, CLIENT_SECRET, TOKEN



def main():
    twitch = Twitch(BOT_USERNAME, CLIENT_ID, TOKEN, 'thestroid')
    twitch.start()


if __name__ == "__main__":
    main()
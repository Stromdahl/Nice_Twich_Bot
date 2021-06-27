
from twitchbot.client import Client
from twitchbot.settings import BOT_USERNAME, CLIENT_ID, CLIENT_SECRET, TOKEN

class TwitchBot:
    def __init__(self) -> None:
        server='irc.chat.twitch.tv'
        port=6667
        username = 'NiceLeaderboard'
        channels = ['thestroid']
        oauth_token = TOKEN
        self.irc_client = Client(server, port, username, channels, oauth_token)

    def connect(self):
        self.irc_client.connect()
        self.irc_client.loop_for_messages()

def main():
    bot = TwitchBot()
    bot.connect()

if __name__ == "__main__":
    main()
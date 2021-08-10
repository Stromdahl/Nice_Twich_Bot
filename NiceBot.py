
from twitchbot import Client
from twitchbot.message import Message
from twitchbot.settings import BOT_USERNAME, CLIENT_ID, CLIENT_SECRET, TOKEN
class TwitchBot(Client):
    def __init__(self) -> None:
        username = 'NiceLeaderboard'
        channels = ['thestroid']
        oauth_token = TOKEN
        super().__init__(username, channels, oauth_token)
        self.command = "!nice"


    def on_message(self, message: Message):
        message = message.text.split()
        command = message[0]
        args = message[1:]
        if command == self.command:
            print(args)

    def run(self):
        super().connect()
        super().loop_for_messages()

def main():
    bot = TwitchBot()
    bot.run()

if __name__ == "__main__":
    main()
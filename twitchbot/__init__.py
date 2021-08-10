from twitchbot.connection import MessageHandler
from .message import Message
from abc import ABC, abstractmethod

class Client(ABC):

    def __init__(self, username, channels, oauth_token) -> None:
        server = 'irc.chat.twitch.tv'
        port=6667
        self.connection = MessageHandler(server, port)
        self.oauth_token = oauth_token
        self.username = username
        self.channels = channels

    def connect(self):
        self.connection.connect()
        self.connection.pass_(self.oauth_token)
        self.connection.nick(self.username)
        for channel in self.channels:
            self.connection.join(channel)
            self.connection.privmsg(channel, 'Im alive!')

    @abstractmethod
    def on_message(self, message:Message):
        raise NotImplementedError("on_message not implemented")

    def loop_for_messages(self):
        while  True:
            messages = self.connection.handle_messages()
            for message in messages:
                self.on_message(message)
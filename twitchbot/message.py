from abc import ABC
import re
class Message:
    raw: str
    user: str
    irc_command: str
    channel: str
    text: str

    def __init__(self, raw, user=None, irc_command=None, channel=None, text=None) -> None:
        self.user = user
        self.channel = channel
        self.text = text
        self.irc_command = irc_command
        self.raw = raw

    def parse_text(self, text):
        text = text.split()
        prefix = text[0]
        return prefix, text[1:]

    def __repr__(self) -> str:
        return f'{self.raw}'

class MessageFactory:
    """
    Factory that is responsible for parsing raw string and create message objects
    The Factory doesn't mainain any of the instaces it creates.
    """
    
    def get_message(self, raw_message) -> Message: 
        result = re.findall(pattern=r':tmi.twitch.tv (\d{3}) (\S+) :(.+)', string=raw_message)
        if result:
            result = result[0]
            message = Message(raw_message, irc_command=result[0], channel=result[1], text=result[2])
            return message

        result = re.findall(pattern=r':(\S+).tmi.twitch.tv (\d{3}) \1 (\S+) :(.+)', string=raw_message)
        if result:
            result = result[0]
            message = Message(raw_message, user=result[0], irc_command=result[1], channel=result[2], text=result[3])
            return message

        result = re.findall(pattern=r':(\S+).tmi.twitch.tv (\d{3}) \1 = (\S+) :(.+)', string=raw_message)
        if result:
            result = result[0]
            message = Message(raw_message, user=result[0], irc_command=result[1], channel=result[2], text=result[3])
            return message

        result = re.findall(pattern=r':(\S+)!\1@\1.tmi.twitch.tv (\S+) (\S+) :(.+)', string=raw_message)
        if result:
            result = result[0]
            message = Message(raw_message, user=result[0], irc_command=result[1], channel=result[2], text=result[3])
            return message

        result = re.findall(pattern=r':(\S+)!\1@\1.tmi.twitch.tv (\S+) (\S+)', string=raw_message)
        if result:
            result = result[0]
            message = Message(raw_message, user=result[0], irc_command=result[1], channel=result[2])
            return message

        result = re.findall(pattern=r'(\S+) :(.+)', string=raw_message)
        if result:
            result = result[0]
            message = Message(raw_message, irc_command=result[0], text=result[1])
            return message

        return None
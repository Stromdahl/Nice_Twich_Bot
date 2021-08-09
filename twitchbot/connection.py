import socket
import logging
import re
from .message import Message

logging.basicConfig(level=logging.INFO)

class IRCError(Exception):
    "An IRC exception"

class ServerConnectionError(IRCError):
    pass

class ServerNotConnectedError(ServerConnectionError):
    pass

class InvalidCharacters(ValueError):
    "Invalid characters were encountered in the message"

class MessageTooLong(ValueError):
    "Message is too long"

class Connection:
    socket = None

    transmit_encoding = 'utf-8'

    def __init__(self, server, port) -> None:
        self.server =server 
        self.port = port
        self.connected = False
        pass

    def connect(self):
        self.socket = socket.socket()
        self.socket.connect((self.server, self.port))
        self.connected = True

    def disconnect(self, msg="Disconnected"):
        """Disconnect the bot"""
        logging.debug(msg)
        self.connected = False

    def encode(self, string):
        return bytes(string, self.transmit_encoding)

    def _prep_message(self, string):
        # The string should not contain any carriage return other than the
        # one added here.
        if '\n' in string:
            raise InvalidCharacters("Carriage returns not allowed in privmsg(text)")
        bytes = self.encode(string) + b'\r\n'
        # According to the RFC http://tools.ietf.org/html/rfc2812#page-6,
        # clients should not transmit more than 512 bytes.
        if len(bytes) > 512:
            raise MessageTooLong("Messages limited to 512 bytes including CR/LF")
        return bytes

    def send_raw(self, string):
        if not self.connect:
            raise ServerNotConnectedError("Not connected")
        try:
            self.socket.send(self._prep_message(string))
            logging.debug(f"< {_hide_pass(string)}")
        except socket.error as err:
            self.disconnect(f'--!!--Socket.error: {err}')

    def receive_data(self):
        data = self.socket.recv(2048).decode()
        return data.split('\r\n')

class ServerConnection(Connection):
    def __init__(self, server, port) -> None:
        super().__init__(server, port)

    def _send_items(self, *items):
        self.send_raw(' '.join(items))

    def pass_(self, password):
        self._send_items('PASS', password)

    def nick(self, username):
        self._send_items('NICK', username)

    def join(self, channel):
        self._send_items('JOIN', f'#{channel}')

    def privmsg(self, channel, text):
        self._send_items('PRIVMSG', f'#{channel}', f':{text}')

    def pong(self, text):
        self._send_items('PONG', text)

    def handle_ping(self):
        self.pong(':tmi.twitch.tv')

    def handle_messages(self):
        privmsg = list()
        for data in self.receive_data():
            logging.debug(f'> {data}')

            if len(data) == 0:
                break

            message = parse_msg(data)
            if message:
                if message.irc_command == 'PING':
                    self.handle_ping()

                if message.irc_command == 'PRIVMSG':
                    logging.info(f'> {message}')
                    privmsg.append(message)
        return privmsg

def _hide_pass(string):
    return string if 'PASS' not in string else 'PASS *************************************'


def parse_msg(msg):
    result = re.findall(pattern=r':tmi.twitch.tv (\d{3}) (\S+) :(.+)', string=msg)
    if result:
        result = result[0]
        message = Message(msg, irc_command=result[0], channel=result[1], text=result[2])
        return message

    result = re.findall(pattern=r':(\S+).tmi.twitch.tv (\d{3}) \1 (\S+) :(.+)', string=msg)
    if result:
        result = result[0]
        message = Message(msg, user=result[0], irc_command=result[1], channel=result[2], text=result[3])
        return message

    result = re.findall(pattern=r':(\S+).tmi.twitch.tv (\d{3}) \1 = (\S+) :(.+)', string=msg)
    if result:
        result = result[0]
        message = Message(msg, user=result[0], irc_command=result[1], channel=result[2], text=result[3])
        return message

    result = re.findall(pattern=r':(\S+)!\1@\1.tmi.twitch.tv (\S+) (\S+) :(.+)', string=msg)
    if result:
        result = result[0]
        message = Message(msg, user=result[0], irc_command=result[1], channel=result[2], text=result[3])
        return message

    result = re.findall(pattern=r':(\S+)!\1@\1.tmi.twitch.tv (\S+) (\S+)', string=msg)
    if result:
        result = result[0]
        message = Message(msg, user=result[0], irc_command=result[1], channel=result[2])
        return message

    result = re.findall(pattern=r'(\S+) :(.+)', string=msg)
    if result:
        result = result[0]
        message = Message(msg, irc_command=result[0], text=result[1])
        return message

    return None


def get_user_from_prefix(prefix):
    domain = prefix.split('!')[0]
    if domain.endswith('.tmi.twitch.tv'):
        return domain.replace('.tmi.twitch.tv', '')
    if 'tmi.twitch.tv' not in domain:
        return domain
    return None
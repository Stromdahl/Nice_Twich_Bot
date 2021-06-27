import socket
import abc
import logging

logging.basicConfig(level=logging.DEBUG)

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
            msg = "Carriage returns not allowed in privmsg(text)"
            raise InvalidCharacters(msg)
        bytes = self.encode(string) + b'\r\n'
        # According to the RFC http://tools.ietf.org/html/rfc2812#page-6,
        # clients should not transmit more than 512 bytes.
        if len(bytes) > 512:
            msg = "Messages limited to 512 bytes including CR/LF"
            raise MessageTooLong(msg)
        return bytes

    def _hide_pass(self, string):
        return string if 'PASS' not in string else 'PASS *************************************'

    def send_raw(self, string):
        if not self.connect:
            raise ServerNotConnectedError("Not connected")
        try:
            self.socket.send(self._prep_message(string))
            logging.debug(f"< {self._hide_pass(string)}")
        except socket.error as err:
            self.disconnect(f'--!!--Socket.error: {err}')

    def recv_data(self):
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

    def handle_messages(self):
        for data in self.recv_data():
            logging.debug(f'> {data}')

class Client:

    def __init__(self, server, port, username, channels, oauth_token) -> None:
        self.connection = ServerConnection(server, port)
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

    def loop_for_messages(self):
        while  True:
             self.connection.handle_messages()
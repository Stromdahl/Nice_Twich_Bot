import irc.bot
import requests

class Twitch(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel
        self.username = username

        self.request_channel_id(channel)
        self.create_irc_connection()

    def request_channel_id(self, channel):
        url = f'https://api.twitch.tv/kraken/users?login={channel}'
        headers = {
            'Client-ID': self.client_id,
            'Accept': 'application/vnd.twitchtv.v5+json'}
        response = requests.get(url, headers=headers).json()
        self.channel_id = response['users'][0]['_id']

    # def get_request(self):
    #     url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
    #     headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
    #     r = requests.get(url, headers=headers).json()
    #     self.connection.privmsg(self.channel, r['display_name'] + ' channel title is currently ' + r['status'])
    #     return requests.get(url, headers=headers).json()

    def create_irc_connection(self):
        server = 'irc.chat.twitch.tv'
        port = 6667
        print (f'Connecting to {server} on port {str(port)}...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, self.token)], self.username, self.username)

    def on_welcome(self, c, e):
        print (f'Joining {self.channel}')

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

        self.send_message("Im online!")

    def on_pubmsg(self, c, e):
        args = e.arguments[0].split()
        if args[0].startswith('!'):
            cmd = args[0][1:]
            self.do_command(e, cmd, args[1:])

    def do_command(self, e, cmd, args):
        if cmd == 'echo':
            message = " ".join(args)
            self.send_message(message)
        if cmd == 'test':
            message = ''
            self.send_message(message)

    def send_message(self, message):
        print(f'Message sent: "{message}"')
        self.connection.privmsg(self.channel, message)
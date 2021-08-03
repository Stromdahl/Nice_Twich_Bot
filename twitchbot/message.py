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
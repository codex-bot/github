from functools import partial


class CommandBase:

    def __init__(self, sdk):
        self.sdk = sdk
        self.bot = None
        self.send = partial(self.sdk.send_text_to_chat, disable_web_page_preview=True)

    def set_bot(self, payload):
        self.bot = payload.get('bot', None)
        self.send = partial(self.sdk.send_text_to_chat, disable_web_page_preview=True, bot=self.bot)

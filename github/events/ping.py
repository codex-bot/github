from .base import EventBase


class EventPing(EventBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = kwargs['headers']

    def process(self, github_payload):
        if self.headers.get('X-GitHub-Event', '') == "ping":
            if self.check_chat():
                self.append_chat()

            self.sdk.log("Ping event occured for the chat #".format())

    def append_chat(self):
        pass

    def check_chat(self):
        return True

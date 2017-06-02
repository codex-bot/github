from .base import EventBase


class EventPing(EventBase):

    def process(self, payload):
        if self.check_chat():
            self.append_chat()

        self.sdk.log("Ping event occured for the chat #".format())

    def append_chat(self):
        pass

    def check_chat(self):
        return True

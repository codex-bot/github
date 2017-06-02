from .base import EventBase


class EventPush(EventBase):

    def process(self, payload):
        self.sdk.log("Push event payload taken")
        print(payload)
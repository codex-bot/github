from data_types.hook import Hook
from data_types.repository import Repository
from data_types.user import User
from .base import EventBase

import math
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])

class EventWatch(EventBase):

    def __init__(self, sdk):
        super(EventWatch, self).__init__(sdk)
        self.hook = None
        self.repository = None
        self.sender = None

    """
    WatchEvent

    Triggered when someone stars your repository.

    https://developer.github.com/v3/activity/events/types/#watchevent
    """

    async def process(self, payload, chat):
        """
        Processes Watch event
        :param payload: JSON object with payload
        :param chat: current chat object
        :return:
        """

        self.sdk.log("Watch event payload taken {}".format(payload))

        try:

            self.repository = Repository(payload['repository'])
            self.sender = User(payload['sender'])

        except Exception as e:
            self.sdk.log('Cannot process WatchEvent payload because of {}'.format(e))

        await self.send(
            chat['chat'],
            '<a href=\"{}\">{}</a> added a {} ⭐️ to <a href=\"{}\">{}</a>'.format(
                self.sender.html_url,
                self.sender.login,
                ordinal(self.sender.repository.stargazers_count),
                self.repository.html_url,
                self.repository.full_name),
            'HTML'
        )

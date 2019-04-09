from data_types.hook import Hook
from data_types.repository import Repository
from data_types.user import User
from .base import EventBase


class EventFork(EventBase):

    def __init__(self, sdk):
        super(EventFork, self).__init__(sdk)
        self.hook = None
        self.repository = None
        self.sender = None

    """
    ForkEvent

    Triggered when someone forks your repository.

    https://developer.github.com/v3/activity/events/types/#forkevent
    """

    async def process(self, payload, chat):
        """
        Processes Fork event
        :param payload: JSON object with payload
        :param chat: current chat object
        :return:
        """

        self.sdk.log("Fork event payload taken {}".format(payload))

        try:

            self.repository = Repository(payload['repository'])
            self.sender = User(payload['sender'])

        except Exception as e:
            self.sdk.log('Cannot process ForkEvent payload because of {}'.format(e))

        await self.send(
            chat['chat'],
            '🦍 <a href=\"{}\">{}</a> forked <a href=\"{}\">{}</a>'.format(
                self.sender.html_url,
                self.sender.login,
                self.repository.html_url,
                self.repository.full_name),
            'HTML'
        )

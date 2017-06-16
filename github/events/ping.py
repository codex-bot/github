from data_types.hook import Hook
from data_types.repository import Repository
from data_types.user import User
from .base import EventBase


class EventPing(EventBase):

    hook = None
    repository = None
    sender = None

    """
    PingEvent

    Triggered when new webhook added.

    https://developer.github.com/webhooks/#ping-event
    """

    async def process(self, payload, chat_id):
        """
        Processes Ping event
        :param payload: JSON object with payload
            zen - Random string of GitHub zen
            hook_id - The ID of the webhook that triggered the ping
            hook - The webhook configuration
        :param chat_id: current user chat token
        :return:
        """

        self.sdk.log("Ping event payload taken {}".format(payload))

        try:

            self.repository = Repository(payload['repository'])
            self.sender = User(payload['sender'])
            self.hook = Hook(payload['hook'])

        except Exception as e:
            self.sdk.log('Cannot process PingEvent payload because of {}'.format(e))

        await self.sdk.send_text_to_chat(
            chat_id,
            'Repository {} successfully linked. Boom.'.format(self.repository.full_name)
        )



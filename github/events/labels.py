import html

from data_types.label import Label
from data_types.repository import Repository
from data_types.user import User
from .base import EventBase


class EventLabels(EventBase):

    def __init__(self, sdk):
        super(EventLabels, self).__init__(sdk)
        self.issue = None
        self.repository = None
        self.sender = None
        self.sdk = sdk

    """
    LabelsEvent

    This event occurs when there is activity relating to labels. 

    https://docs.github.com/developers/webhooks-and-events/webhooks/webhook-events-and-payloads#label
    """

    async def process(self, payload, chat):
        """
        Processes Labels event
        :param payload: JSON object with payload
        :param chat: current chat object
        :return:
        """

        self.sdk.log("Labels event payload taken")

        try:
            self.label = Label(payload['label'])
            self.repository = Repository(payload['repository'])
            self.sender = User(payload['sender'])

        except Exception as e:
            self.sdk.log('Cannot process LabelsEvent payload because of {}'.format(e))

        action = payload['action']

        available_actions = {
            'created': self.created,
            # 'deleted': self.deleted,
            # 'edited': self.edited
        }

        if action not in available_actions:
            self.sdk.log('Unsupported Labels action: {}'.format(action))
            return

        # call action handler
        await available_actions[action](chat['chat'], payload)

    async def created(self, chat_id, payload):
        """
        Labels created action
        :param chat_id: Current user chat token
        :param payload: GitHub payload
        :return:
        """

        message = f"✏️ {self.sender.login} created a new label [<a href=\"{self.label.url}\">{self.label.name}</a>]\n\n{self.label.url}"

        await self.send(
            chat_id,
            message,
            'HTML'
        )

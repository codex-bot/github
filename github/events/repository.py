from data_types.organization import Organization
from data_types.repository import Repository
from data_types.user import User
from .base import EventBase


class EventRepository(EventBase):

    def __init__(self, sdk):
        super(EventRepository, self).__init__(sdk)
        self.hook = None
        self.repository = None
        self.sender = None

    """
    RepositoryEvent

    Triggered when someone creates a new repository in your organization.

    https://docs.github.com/en/developers/webhooks-and-events/webhook-events-and-payloads#repository
    """

    async def process(self, payload, chat):
        """
        Processes Repository event
        :param payload: JSON object with payload
        :param chat: current chat object
        :return:
        """

        self.sdk.log("Repository event payload taken {}".format(payload))

        try:

            self.repository = Repository(payload['repository'])
            self.organization = Organization(payload['organization'])
            self.sender = User(payload['sender'])

        except Exception as e:
            self.sdk.log('Cannot process RepositoryEvent payload because of {}'.format(e))

        await self.send(
            chat['chat'],
            '🦍 <a href=\"{}\">{}</a> created a repository <a href=\"{}\">{}</a> in the {} organization'.format(
                self.sender.html_url,
                self.sender.login,
                self.repository.html_url,
                self.repository.full_name,
                self.organization.login),
            'HTML'
        )

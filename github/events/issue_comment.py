import html

from data_types.issue import Issue
from data_types.issue_comment import IssueComment
from data_types.repository import Repository
from data_types.user import User
from .base import EventBase


class EventIssueComment(EventBase):

    def __init__(self, sdk):
        super(EventIssueComment, self).__init__(sdk)
        self.issue = None
        self.repository = None
        self.sender = None
        self.sdk = sdk

    """
    IssueCommentEvent

    Triggered when an issue comment is created, edited, or deleted.

    https://developer.github.com/v3/activity/events/types/#issuecommentevent
    """

    async def process(self, payload, chat):
        """
        Processes IssueComment event
        :param payload: JSON object with payload
        :param chat: current chat object
        :return:
        """

        self.sdk.log("IssueComment event payload taken")

        try:
            self.issue = Issue(payload['issue'])
            self.comment = IssueComment(payload['comment'])
            self.repository = Repository(payload['repository'])
            self.sender = User(payload['sender'])

        except Exception as e:
            self.sdk.log('Cannot process IssueCommentEvent payload because of {}'.format(e))

        action = payload['action']

        available_actions = {
            'created': self.created
        }

        if action not in available_actions:
            self.sdk.log('Unsupported IssueComment action: {}'.format(action))
            return

        # call action handler
        await available_actions[action](chat['chat'], payload)

    async def created(self, chat_id, payload):
        """
        IssueComment created action
        :param chat_id: Current user chat token
        :param payload: GitHub payload
        :return:
        """

        message = "📝 {} created a new comment to the issue «<a href=\"{}\">{}</a>» [<a href=\"{}\">{}</a>]".format(
                        self.sender.login,
                        self.issue.html_url,
                        html.escape(self.issue.title),
                        self.repository.html_url,
                        self.repository.name
                    ) + "\n\n"

        message += self.comment.html_url

        await self.send(
            chat_id,
            message,
            'HTML'
        )

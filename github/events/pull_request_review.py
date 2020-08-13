import html

from data_types.pull_request_review import PullRequestReview
from data_types.pull_request import PullRequest
from data_types.repository import Repository
from data_types.user import User
from .base import EventBase


class EventPullRequestReview(EventBase):

    def __init__(self, sdk):
        super(EventPullRequestReview, self).__init__(sdk)
        self.pull_request = None
        self.repository = None
        self.sender = None
        self.sdk = sdk

    """
    PullRequestReviewEvent

    Triggered when a pull request review is submitted into a non-pending state,
    the body is edited, or the review is dismissed.

    https://developer.github.com/v3/activity/events/types/#pullrequestevent
    """

    async def process(self, payload, chat):
        """
        Processes Pull Request Review event
        :param payload: JSON object with payload
            action          string  - The action that was performed. Can be "submitted", "edited", or "dismissed".
            pull_request    object  - Pull request object
            review          object  - The review that was affected.
            changes[body][from]     - The previous version of the body if the action was "edited".

        :param chat: current chat object
        :return:
        """

        self.sdk.log("PullRequestReview event payload taken {}".format(payload))

        try:
            self.pull_request = PullRequest(payload['pull_request'])
            self.repository = Repository(payload['repository'])
            self.sender = User(payload['sender'])
            self.review = PullRequestReview(payload['review'])
            self.action = payload['action']

        except Exception as e:
            self.sdk.log('Cannot process PullRequestReview payload because of {}'.format(e))

        state = self.review.state

        available_states = {
            'approved': self.approved,
            'commented': self.commented,
            'changes_requested': self.changes_requested
        }

        if state not in available_states:
            self.sdk.log('Unsupported PullRequestReview state: {}'.format(state))
            return

        if self.action != "submitted":
            self.sdk.log('PullRequestReview action is not equal "submitted": {}'.format(state))
            return

        # call action handler
        await available_states[state](chat['chat'], payload)

    async def approved(self, chat_id, payload):
        """
        Pull Request Review approved state
        :param chat_id: Current user chat token
        :param payload: GitHub payload
        :return:
        """

        message = "✅ {name} approved «<code>{pull_request}</code>».".format(
                    name=self.sender.login,
                    pull_request=self.pull_request.title
        ) + "\n\n"

        if self.review.body is not None:
            message += html.escape(self.review.body) + "\n\n"

        message += self.pull_request.html_url

        await self.send(
            chat_id,
            message,
            'HTML'
        )

    async def changes_requested(self, chat_id, payload):
        """
        Pull Request Review changes_requested state
        :param chat_id: Current user chat token
        :param payload: GitHub payload
        :return:
        """

        message = "❌ {name} requested changes in «<code>{pull_request}</code>».".format(
                    name=self.sender.login,
                    pull_request=self.pull_request.title
        ) + "\n\n"

        if self.review.body is not None:
            message += html.escape(self.review.body) + "\n\n"

        message += self.pull_request.html_url

        await self.send(
            chat_id,
            message,
            'HTML'
        )

    async def commented(self, chat_id, payload):
        """
        Pull Request Review commented state
        :param chat_id: Current user chat token
        :param payload: GitHub payload
        :return:
        """

        message = "💬 {name} reviewed «<code>{pull_request}</code>».".format(
                    name=self.sender.login,
                    pull_request=self.pull_request.title
        ) + "\n\n"

        if self.review.body is not None:
            message += html.escape(self.review.body) + "\n\n"

        message += self.pull_request.html_url

        await self.send(
            chat_id,
            message,
            'HTML'
        )

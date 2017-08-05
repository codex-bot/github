import html

from data_types.pull_request import PullRequest
from data_types.repository import Repository
from data_types.user import User
from .base import EventBase


class EventPullRequest(EventBase):

    def __init__(self, sdk):
        self.pull_request = None
        self.repository = None
        self.sender = None
        self.sdk = sdk

    """
    PullRequestEvent

    Triggered when a pull request is assigned, unassigned, labeled, unlabeled, opened, edited, closed,
    reopened, or synchronized. Also triggered when a pull request review is requested,
    or when a review request is removed.

    https://developer.github.com/v3/activity/events/types/#pullrequestevent
    """

    async def process(self, payload, chat_id):
        """
        Processes Pull Request event
        :param payload: JSON object with payload
            action  string      - Can be one of "assigned", "unassigned", "review_requested", "review_request_removed",
                                "labeled", "unlabeled", "opened", "edited", "closed", or "reopened".
                                If the action is "closed" and the merged key is false, the pull request was closed
                                with unmerged commits. If the action is "closed" and the merged key is true,
                                the pull request was merged. While webhooks are also triggered
                                when a pull request is synchronized, Events API timelines don't include
                                pull request events with the "synchronize" action.
            number  integer     - The pull request number.

            changes object          - The changes to the comment if the action was "edited".
            changes[title][from]    - The previous version of the title if the action was "edited".
            changes[body][from]     - The previous version of the body if the action was "edited".

            pull_request        - Pull request object

        :param chat_id: current user chat token
        :return:
        """

        self.sdk.log("PullRequest event payload taken {}".format(payload))

        try:
            self.pull_request = PullRequest(payload['pull_request'])
            self.repository = Repository(payload['repository'])
            self.sender = User(payload['sender'])

        except Exception as e:
            self.sdk.log('Cannot process PullRequest payload because of {}'.format(e))

        action = payload['action']

        available_actions = {
            'opened': self.opened,
            'closed': self.closed,
            'review_requested': self.review_requested
        }

        if action not in available_actions:
            self.sdk.log('Unsupported PullRequest action: {}'.format(action))
            return

        # call action handler
        await available_actions[action](chat_id, payload)

    async def opened(self, chat_id, payload):
        """
        Pull Request opened action
        :param chat_id: Current user chat token
        :param payload: GitHub payload
        :return:
        """

        message = "😼 {name} opened pull request «<code>{title}</code>» " \
                  "from <b>{head}</b> to <b>{base}</b>" \
                  "[<a href=\"{repository_url}\">{repository_name}</a>]".format(
                    name=self.sender.login,
                    title=html.escape(self.pull_request.title),
                    head=self.pull_request.head.ref,
                    base=self.pull_request.base.ref,
                    repository_url=self.repository.html_url,
                    repository_name=self.repository.full_name
        ) + "\n\n"

        if len(self.pull_request.body):
            message += html.escape(self.pull_request.body) + "\n\n"

        message += self.pull_request.html_url

        await self.sdk.send_text_to_chat(
            chat_id,
            message,
            'HTML'
        )

    async def closed(self, chat_id, payload):
        """
        Close pull request action
        :param chat_id: Current user chat token
        :param payload: GitHub payload
        :return:
        """
        message = "😾 {name} closed pull request «<code>{title}</code>» " \
                  "from <b>{head}</b> to <b>{base}</b>" \
                  "[<a href=\"{repository_url}\">{repository_name}</a>]".format(
                    name=self.sender.login,
                    title=html.escape(self.pull_request.title),
                    head=self.pull_request.head.ref,
                    base=self.pull_request.base.ref,
                    repository_url=self.repository.html_url,
                    repository_name=self.repository.full_name
        ) + "\n\n"

        if len(self.pull_request.body):
            message += html.escape(self.pull_request.body) + "\n\n"

        message += self.pull_request.html_url

        await self.sdk.send_text_to_chat(
            chat_id,
            message,
            'HTML'
        )

    async def review_requested(self, chat_id, payload):
        """
        Pull request review requested action
        :param chat_id: Current user chat token
        :param payload: GitHub payload
        :return:
        """

        requested_reviewer = self.pull_request.requested_reviewer

        message = "🙀 {name} requested <code>{requested_reviewer}</code>'s review for pull request" \
                  "«<a href=\"{request_url}\">{request_title}</a>» " \
                  "[<a href=\"{repository_url}\">{repository_name}</a>]".format(
                    name=self.sender.login,
                    requested_reviewer=requested_reviewer.login,
                    request_url=self.pull_request.html_url,
                    request_title=html.escape(self.pull_request.title),
                    repository_url=self.repository.html_url,
                    repository_name=self.repository.full_name
        )

        await self.sdk.send_text_to_chat(
            chat_id,
            message,
            'HTML'
        )

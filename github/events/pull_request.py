import html

from data_types.pull_request import PullRequest
from data_types.repository import Repository
from data_types.organization import Organization
from data_types.user import User
from data_types.team import Team
from data_types.label import Label
from .base import EventBase


class EventPullRequest(EventBase):

    def __init__(self, sdk):
        super(EventPullRequest, self).__init__(sdk)
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

    async def process(self, payload, chat):
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

        :param chat: current chat object
        :return:
        """

        self.sdk.log("PullRequest event payload taken {}".format(payload))

        try:
            self.pull_request = PullRequest(payload['pull_request'])
            self.repository = Repository(payload['repository'])
            self.organization = Organization(payload['organization'])
            self.sender = User(payload['sender'])

        except Exception as e:
            self.sdk.log('Cannot process PullRequest payload because of {}'.format(e))

        action = payload['action']

        available_actions = {
            'opened': self.opened,
            'reopened': self.reopened,
            'closed': self.closed,
            'review_requested': self.review_requested,
            'labeled': self.labeled
        }

        if action not in available_actions:
            self.sdk.log('Unsupported PullRequest action: {}'.format(action))
            return

        # call action handler
        await available_actions[action](chat['chat'], payload)

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

        if self.pull_request.body is not None and len(self.pull_request.body):
            message += html.escape(self.pull_request.body) + "\n\n"

        message += self.pull_request.html_url

        await self.send(
            chat_id,
            message,
            'HTML'
        )

    async def reopened(self, chat_id, payload):
        """
        Pull Request opened action
        :param chat_id: Current user chat token
        :param payload: GitHub payload
        :return:
        """

        message = "😼 {name} reopened pull request «<code>{title}</code>» " \
                  "from <b>{head}</b> to <b>{base}</b>" \
                  "[<a href=\"{repository_url}\">{repository_name}</a>]".format(
                    name=self.sender.login,
                    title=html.escape(self.pull_request.title),
                    head=self.pull_request.head.ref,
                    base=self.pull_request.base.ref,
                    repository_url=self.repository.html_url,
                    repository_name=self.repository.full_name
        ) + "\n\n"

        if self.pull_request.body is not None and len(self.pull_request.body):
            message += html.escape(self.pull_request.body) + "\n\n"

        message += self.pull_request.html_url

        await self.send(
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
        message = "{merged_emoji} {name} closed pull request «<code>{title}</code>» " \
                  "from <b>{head}</b> to <b>{base}</b>" \
                  "[<a href=\"{repository_url}\">{repository_name}</a>]".format(
                    merged_emoji="😺" if self.pull_request.merged else "😾",
                    name=self.sender.login,
                    title=html.escape(self.pull_request.title),
                    head=self.pull_request.head.ref,
                    base=self.pull_request.base.ref,
                    repository_url=self.repository.html_url,
                    repository_name=self.repository.full_name
        ) + "\n\n"

        if self.pull_request.body is not None and len(self.pull_request.body):
            message += html.escape(self.pull_request.body) + "\n\n"

        message += self.pull_request.html_url

        await self.send(
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

        # get user.login or team.name
        requested_reviewer_name = ''

        if payload.get('requested_reviewer'):
            requested_reviewer = User(payload['requested_reviewer'])
            requested_reviewer_name = requested_reviewer.login

        if payload.get('requested_team'):
            requested_reviewer = Team(payload['requested_team'])
            requested_reviewer_name = requested_reviewer.name

        message = "🙀 {name} requested <code>{requested_reviewer}</code>'s review " \
                  "for pull request «<a href=\"{request_url}\">{request_title}</a>» " \
                  "[<a href=\"{repository_url}\">{repository_name}</a>]".format(
                    name=self.sender.login,
                    requested_reviewer=requested_reviewer_name,
                    request_url=self.pull_request.html_url,
                    request_title=html.escape(self.pull_request.title),
                    repository_url=self.repository.html_url,
                    repository_name=self.repository.full_name
        )

        await self.send(
            chat_id,
            message,
            'HTML'
        )

    async def labeled(self, chat_id, payload):
        """
        Pull request labeled action
        :param chat_id: Current user chat token
        :param payload: GitHub payload
        :return:
        """

        label = Label(payload['label'])

        message = "🏷 PR <a href=\"{pull_request_url}\">{pull_request_title}</a> was labeled as <b>{label}</b> — " \
                  "{author} at {organization_login}/{repository_name}".format(
                        pull_request_url=self.pull_request.html_url,
                        pull_request_title=html.escape(self.pull_request.title),
                        label=label.name,
                        author=self.sender.login,
                        organization_login=self.organization.login,
                        repository_name=self.repository.name
                    )

        await self.send(
            chat_id,
            message,
            'HTML'
        )

import html

from data_types.issue import Issue
from data_types.repository import Repository
from data_types.organization import Organization
from data_types.user import User
from data_types.label import Label
from .base import EventBase


class EventIssues(EventBase):

    def __init__(self, sdk):
        super(EventIssues, self).__init__(sdk)
        self.issue = None
        self.repository = None
        self.sender = None
        self.sdk = sdk

    """
    IssuesEvent

    Triggered when an issue is assigned, unassigned, labeled, unlabeled,
    opened, edited, milestoned, demilestoned, closed, or reopened.

    https://developer.github.com/v3/activity/events/types/#issuesevent
    """

    async def process(self, payload, chat):
        """
        Processes Issues event
        :param payload: JSON object with payload
        :param chat: current chat object
        :return:
        """

        self.sdk.log("Issues event payload taken")

        try:
            self.issue = Issue(payload['issue'])
            self.repository = Repository(payload['repository'])
            self.organization = Repository(payload['organization'])
            self.sender = User(payload['sender'])

        except Exception as e:
            self.sdk.log('Cannot process IssuesEvent payload because of {}'.format(e))

        action = payload['action']

        available_actions = {
            'opened': self.opened,
            'closed': self.closed,
            'assigned': self.assigned,
            'labeled': self.labeled
        }

        if action not in available_actions:
            self.sdk.log('Unsupported Issues action: {}'.format(action))
            return

        # call action handler
        await available_actions[action](chat['chat'], payload)

    async def opened(self, chat_id, payload):
        """
        Issue opened action
        :param chat_id: Current user chat token
        :param payload: GitHub payload
        :return:
        """

        message = "✏️ {} opened new issue «<code>{}</code>» [<a href=\"{}\">{}</a>]".format(
            self.sender.login,
            html.escape(self.issue.title),
            self.repository.html_url,
            self.repository.name
        ) + "\n\n"

        # if len(self.issue.body):
        #     message += html.escape(self.issue.body) + "\n\n"

        message += self.issue.html_url

        await self.send(
            chat_id,
            message,
            'HTML'
        )

    async def closed(self, chat_id, payload):
        """
        Close issue action
        :param chat_id: Current user chat token
        :param payload: GitHub payload
        :return:
        """
        message = "☑️ {} closed issue «<code>{}</code>» [<a href=\"{}\">{}</a>]".format(
            self.sender.login,
            html.escape(self.issue.title),
            self.repository.html_url,
            self.repository.name
        ) + "\n\n"

        # if len(self.issue.body):
        #     message += html.escape(self.issue.body) + "\n\n"

        message += self.issue.html_url

        await self.send(
            chat_id,
            message,
            'HTML'
        )

    async def assigned(self, chat_id, payload):
        """
        Issue assigned action
        :param chat_id: Current user chat token
        :param payload: GitHub payload
        :return:
        """

        assignee = User(payload['assignee'])

        message = "📌 {assignee} has been assigned to the issue «<code>{issue_title}</code>» " \
                  "by {author} [<a href=\"{repository_html}\">{repository_name}</a>]".format(
                        assignee=assignee.login,
                        author=self.sender.login,
                        issue_title=html.escape(self.issue.title),
                        repository_html=self.repository.html_url,
                        repository_name=self.repository.name
                    ) + "\n\n"

        message += self.issue.html_url

        await self.send(
            chat_id,
            message,
            'HTML'
        )

    async def labeled(self, chat_id, payload):
        """
        Issue labeled action
        :param chat_id: Current user chat token
        :param payload: GitHub payload
        :return:
        """

        label = Label(payload['label'])

        message = "🏷 Issue <a href=\"{issue_url}\">{issue_title}</a> was labeled as <b>{label}</b> — " \
                  "{author} at {organization_login}/{repository_name}".format(
                        issue_url=self.issue.html_url,
                        issue_title=html.escape(self.issue.title),
                        label=label.name,
                        author=self.sender.login,
                        organization_login=self.organization.login,
                        repository_name=self.repository.name
                    ) + "\n\n"

        message += self.issue.html_url

        await self.send(
            chat_id,
            message,
            'HTML'
        )

import html

from github.data_types.issue import Issue
from github.data_types.repository import Repository
from github.data_types.user import User
from .base import EventBase


class EventIssues(EventBase):

    issue = None
    repository = None
    sender = None

    """
    IssuesEvent

    Triggered when an issue is assigned, unassigned, labeled, unlabeled,
    opened, edited, milestoned, demilestoned, closed, or reopened.

    https://developer.github.com/v3/activity/events/types/#issuesevent
    """

    async def process(self, payload, chat_id):
        """
        Processes Issues event
        :param payload: JSON object with payload
        :param chat_id: current user chat token
        :return:
        """

        self.sdk.log("Issues event payload taken")

        try:
            self.issue = Issue(payload['issue'])
            self.repository = Repository(payload['repository'])
            self.sender = User(payload['sender'])

        except Exception as e:
            self.sdk.log('Cannot process IssuesEvent payload because of {}'.format(e))

        action = payload['action']

        available_actions = {
            'opened': self.opened,
            'closed': self.closed,
            'assigned': self.assigned
        }

        if action not in available_actions:
            self.sdk.log('Unsupported Issues action: {}'.format(action))

        # call action handler
        await available_actions[action](chat_id, payload)

    async def opened(self, chat_id, payload):
        """
        Issue opened action
        :param chat_id: Current user chat token
        :param payload: GitHub payload
        :return:
        """

        message = "{} opened new issue «<code>{}</code>» [<a href=\"{}\">{}</a>]".format(
                        self.sender.login,
                        self.issue.title,
                        self.repository.html_url,
                        self.repository.name
                    ) + "\n\n"

        if len(self.issue.body):
            message += html.escape(self.issue.body) + "\n\n"

        message += self.issue.html_url

        await self.sdk.send_to_chat(
            chat_id,
            message
        )

    async def closed(self, chat_id, payload):
        """
        Close issue action
        :param chat_id: Current user chat token
        :param payload: GitHub payload
        :return:
        """
        message = "{} closes issue «<code>{}</code>» [<a href=\"{}\">{}</a>]".format(
            self.sender.login,
            self.issue.title,
            self.repository.html_url,
            self.repository.name
        ) + "\n\n"

        if len(self.issue.body):
            message += html.escape(self.issue.body) + "\n\n"

        message += self.issue.html_url

        await self.sdk.send_to_chat(
            chat_id,
            message
        )

    async def assigned(self, chat_id, payload):
        """
        Issue assigned action
        :param chat_id: Current user chat token
        :param payload: GitHub payload
        :return:
        """

        assignee = User(payload['assignee'])

        message = "{assignee} has been assigned to the issue «<code>{issue_title}</code>» by {author} [{repository_name}]".format(
            assignee=assignee.login,
            author=self.sender.login,
            issue_title=self.issue.title,
            repository_name=self.repository.name
        ) + "\n\n"

        message += self.issue.html_url

        await self.sdk.send_to_chat(
            chat_id,
            message
        )

from github.data_types.issue import Issue
from github.data_types.repository import Repository
from .base import EventBase


class EventIssues(EventBase):

    action = None
    issue = None
    repository = None

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

        # Store chat_id to use it next in action handlers
        self.chat_id = chat_id

        try:
            self.issue = Issue(payload['issue'])
            self.repository = Repository(payload['repository'])

        except Exception as e:
            self.sdk.log('Cannot process IssuesEvent payload')

        action = payload['action']

        available_actions = {
            'opened': self.opened,
            'closed': self.closed
        }

        if action not in available_actions:
            self.sdk.log('Unsupported Issues action: {}'.format(action))

        # call action handler
        await available_actions[action]()

        # author = self.data['sender']['login']
        # issue = self.data['issue']
        # action = self.data['action']
        # repository_name = self.data['repository']['full_name']
        #
        # if action == "opened" or action == "closed":
        #     template.append("{} {} {} {}issue «<code>{}</code>» [<a href=\"{}\">{}</a>]".format(
        #         "👉" if action == "opened" else "✅",
        #         author,
        #         action,
        #         "new " if action == "opened" else "",
        #         issue['title'],
        #         'https://github.com/' + repository_name,
        #         repository_name
        #     ))
        #     template.append("\n%s\n" % html.escape(issue['body'])) if len(issue['body']) else template.append("")
        #     template.append("%s\n" % issue['html_url'])
        #
        # if action == 'assigned':
        #     assignee = self.data['assignee']['login']
        #
        #     template.append(
        #         '📌 {assignee} has been assigned to the issue «<code>{issue_title}</code>» by {author} [{repository_name}]'.format(
        #             author=author,
        #             assignee=assignee,
        #             issue_title=issue['title'],
        #             repository_name=repository_name
        #         ))
        #     template.append('')
        #     template.append(issue['html_url'])

        # return '\n'.join(template)

    async def opened(self):
        print('opened')

        await self.sdk.send_to_chat(
            self.chat_id,
            "Issue opened"
        )

    async def closed(self):
        print('closed')

        await self.sdk.send_to_chat(
            self.chat_id,
            "Issue closed"
        )
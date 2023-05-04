import html

from data_types.repository import Repository
from data_types.organization import Organization
from data_types.user import User
from data_types.workflow import Workflow
from data_types.workflow_run import WorkflowRun
from .base import EventBase


class EventWorkflowRun(EventBase):

    def __init__(self, sdk):
        super(EventWorkflowRun, self).__init__(sdk)
        self.workflow_run = None
        self.repository = None
        self.sender = None
        self.sdk = sdk

    """
    WorkflowRunEvent

    This event occurs when there is activity relating to a run of a GitHub Actions workflow. 

    https://docs.github.com/webhooks-and-events/webhooks/webhook-events-and-payloads#workflow_run
    """

    async def process(self, payload, chat):
        """
        Processes Workflow Run event
        :param payload: JSON object with payload
            action  string      - Can be one of "completed", "in_progress", "requested".
            workflow object
            workflow_run object
            repository object
            organization object
            sender object

        :param chat: current chat object
        :return:
        """

        self.sdk.log("WorkflowRun event payload taken {}".format(payload))

        try:
            self.workflow = Workflow(payload['workflow'])
            self.workflow_run = WorkflowRun(payload['workflow_run'])
            self.repository = Repository(payload['repository'])
            self.organization = Organization(payload['organization'])
            self.sender = User(payload['sender'])

        except Exception as e:
            self.sdk.log('Cannot process WorkflowRun payload because of {}'.format(e))

        action = payload['action']

        available_actions = {
            'completed': self.completed
        }

        if action not in available_actions:
            self.sdk.log('Unsupported WorkflowRun action: {}'.format(action))
            return

        # call action handler
        await available_actions[action](chat['chat'], payload)

    async def completed(self, chat_id, payload):
        """
        Workflow Run completed action
        :param chat_id: Current user chat token
        :param payload: GitHub payload
        :return:
        """

        if self.workflow_run.conclusion == "success":
            message = f"⚙️ Workflow <a href=\"{self.workflow_run.html_url}\">{self.workflow.name}</a> ✅"
        else:
            message = f"⚙️ Workflow <a href=\"{self.workflow_run.html_url}\">{self.workflow.name}</a> {self.workflow_run.conclusion} ❌"

        await self.send(
            chat_id,
            message,
            'HTML'
        )

class WorkflowRun:
    """
    GitHub WorkflowRun

    https://docs.github.com/en/rest/actions/workflow-runs?apiVersion=2022-11-28#get-a-workflow-run

    Attributes:
        id: GitHub internal id
        name: Workflow short name like "Build and push docker image"
        head_branch: Branch name like "stage"
        path: Path to the workflow file like ".github/workflows/build-and-push-docker-image.yml"
        status: Can be one of: "requested, in_progress, completed, queued, pending, waiting"
        conclusion: Can be one of: "success, failure, neutral, cancelled, timed_out, action_required, stale, null, skipped"
        event: Triggering event like "push"
        created_at: Workflow created date like "2022-01-12T10:09:23.000Z"
        updated_at : Workflow updated date
        url: Url to workflow run on API (api.github.com)
        html_url: Public URL on github.com
    """

    def __init__(self, data):

        # Internal GitHub id
        self.id = data.get('id', 0)

        self.name = data.get('name', '')
        self.head_branch = data.get('head_branch', '')
        self.path = data.get('path', '')
        self.status = data.get('status', '')
        self.conclusion = data.get('conclusion', '')
        self.event = data.get('event', '')

        self.created_at = data.get('created_at', '')
        self.updated_at = data.get('updated_at', '')

        # Links
        self.url = data.get('url', '')
        self.html_url = data.get('html_url', '')

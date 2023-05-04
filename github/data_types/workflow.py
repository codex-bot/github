class Workflow:
    """
    GitHub Workflow

    https://docs.github.com/en/rest/actions/workflow-runs?apiVersion=2022-11-28#get-a-workflow-run

    Attributes:
        id: GitHub internal id
        name: Workflow short name like "Build and push docker image"
        path: Path to the workflow file like ".github/workflows/build-and-push-docker-image.yml"
        state: Workflow state: https://docs.github.com/en/graphql/reference/enums#workflowstate
        created_at: Workflow created date like "2022-01-12T10:09:23.000Z"
        updated_at : Workflow updated date
        url: Url to workflow on API (api.github.com)
        html_url: Public URL on github.com
        badge_url: SVG badge of the workflow result
    """

    def __init__(self, data):

        # Internal GitHub id
        self.id = data.get('id', 0)

        self.name = data.get('name', '')
        self.path = data.get('path', '')
        self.state = data.get('state', '')

        self.created_at = data.get('created_at', '')
        self.updated_at = data.get('updated_at', '')

        # Links
        self.url = data.get('url', '')
        self.html_url = data.get('html_url', '')
        self.badge_url = data.get('badge_url', '')

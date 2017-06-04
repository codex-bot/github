from github.data_types.user import User


class Issue:
    """
    GitHub Issue

    https://developer.github.com/v3/issues/

    Attributes:
        id: Issue id
        title: Issue title
        body: Issue body text
        html_url: Public URL for issue on github.com
        number: Issue's number in repository
        state: open|closed
        user: Issue opener User object
        labels: List of labels for issue ([id, name, url, color, default])

        created_at: Opening time
        closed_at: Closing time. Null by default
        updated_at: Updating time

        pull_request_url: If issue linked in pull request, stores its public URL
    """

    def __init__(self, data):

        # Internal GitHub id
        self.id = data.get('id', 0)

        # Title and Body
        self.title = data.get('title', '')
        self.body = data.get('body', '')

        # Public link
        self.html_url = data.get('html_url', '')

        # Number in repository
        self.number = data.get('number', '')

        # Who opened
        self.user = None
        if 'user' in data:
            self.user = User(data['user'])

        # Who closed
        self.closed_by = None
        if 'closed_by' in data:
            self.closed_by = User(data['closed_by'])

        # Labels
        self.labels = data.get('labels', '')

        # Dates
        self.created_at = data.get('created_at', '')
        self.closed_at = data.get('closed_at', '')
        self.updated_at = data.get('updated_at', '')

        self.state = data.get('state', '')

        # Linked pull request
        self.pull_request_url = ''
        if 'pull_request' in data:
            self.pull_request_url = data['pull_request'].get('html_url', '')

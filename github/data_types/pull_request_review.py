from data_types.user import User


class PullRequestReview:
    """
    GitHub Pull Request Review

    https://developer.github.com/v3/pulls/reviews/

    Attributes:
        id: Review id
        body: Review body text
        html_url: Public URL for issue on github.com
        state: approved|commented|changes_requested
        user: Review author User object

        submitted_at: Submitted time

        pull_request_url: If issue linked in pull request, stores its public URL
    """

    def __init__(self, data):

        # Internal GitHub id
        self.id = data.get('id', 0)

        # Who create
        self.user = None
        if 'user' in data:
            self.user = User(data['user'])

        # Body
        self.body = data.get('body', '')

        # Dates
        self.submitted_at = data.get('submitted_at', '')

        self.html_url = data.get('html_url', '')

        # Review result
        self.state = data.get('state', '')

        # Linked pull request
        self.pull_request_url = ''
        if 'pull_request' in data:
            self.pull_request_url = data['pull_request'].get('html_url', '')

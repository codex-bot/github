from data_types.user import User


class IssueComment:
    """
    GitHub IssueComment

    https://developer.github.com/v3/issues/comments/

    Attributes:
        id: Comment id
        node_id: Node id
        url: API URL for issue comment on github.com
        html_url: Public URL for issue comment on github.com
        body: Issue comment body text
        user: Issue opener User object

        created_at: Opening time
        closed_at: Closing time. Null by default
        updated_at: Updating time

        issue_url: Issue public URL
    """

    def __init__(self, data):

        # Internal GitHub id
        self.id = data.get('id', 0)
        self.node_id = data.get('node_id', 0)

        # Commented issue
        self.issue_url = data.get('issue_url', '')

        # Body
        self.body = data.get('body', '')

        # Public link
        self.url = data.get('url', '')
        self.html_url = data.get('html_url', '')

        # Who opened
        self.user = None
        if 'user' in data:
            self.user = User(data['user'])

        # Dates
        self.created_at = data.get('created_at', '')
        self.closed_at = data.get('closed_at', '')
        self.updated_at = data.get('updated_at', '')

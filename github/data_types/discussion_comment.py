from data_types.user import User


class DiscussionComment:
    """
    GitHub DiscussionComment

    https://developer.github.com/v3/discussions/comments/

    Attributes:
        id: Comment id
        node_id: Node id
        html_url: Public URL for discussion comment on github.com
        body: Discussion comment body text
        user: Discussion comment creator User object

        created_at: Opening time
        updated_at: Updating time
    """

    def __init__(self, data):

        # Internal GitHub id
        self.id = data.get('id', 0)
        self.node_id = data.get('node_id', 0)

        # Body
        self.body = data.get('body', '')

        # Public link
        self.html_url = data.get('html_url', '')

        # Who created
        self.user = None
        if 'user' in data:
            self.user = User(data['user'])

        # Dates
        self.created_at = data.get('created_at', '')
        self.updated_at = data.get('updated_at', '')

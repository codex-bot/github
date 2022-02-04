from data_types.user import User


class Discussion:
    """
    GitHub Discussions

    Attributes:
        id: Discussion id
        title: Discussion title
        body: Issue body text
        html_url: Public URL for discussion on github.com
        number: Issue's number in repository
        user: Issue opener User object

        created_at: Opening time
    """

    def __init__(self, data):

        # Internal GitHub id
        self.id = data.get('id', 0)

        # Title and Body
        self.title = data.get('title', '')

        # Public link
        self.html_url = data.get('html_url', '')

        # Number in repository
        self.number = data.get('number', '')

        # Who created
        self.user = None
        if 'user' in data:
            self.user = User(data['user'])

        # Dates
        self.created_at = data.get('created_at', '')
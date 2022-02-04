from data_types.user import User
from data_types.category import Category

class Discussion:
    """
    GitHub Discussions

    Attributes:
        id: Discussion id
        title: Discussion title
        html_url: Public URL for discussion on github.com
        number: Discussion's number in repository
        user: Discussion creator User object
    """

    def __init__(self, data):

        # Internal GitHub id
        self.id = data.get('id', 0)

        # Title
        self.title = data.get('title', '')

        # Public link
        self.html_url = data.get('html_url', '')

        # Number in repository
        self.number = data.get('number', '')

        # Category
        self.category = Category(data['category'])

        # Who created
        self.user = None
        if 'user' in data:
            self.user = User(data['user'])
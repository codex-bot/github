from github.data_types.repository import Repository
from github.data_types.user import User


class Branch:
    """
    GitHub Branch object

    Attributes:
        ref:    branch name
        sha:    branch token
        user:   branch creator
        repo:   repository object

    """

    def __init__(self, data):

        self.ref = data.get('ref', '')
        self.sha = data.get('sha', '')

        # Who opened
        self.user = None
        if 'user' in data:
            self.user = User(data['user'])

        # Who merged and sends
        self.repo = None
        if 'repo' in data:
            self.repo = Repository(data['repo'])

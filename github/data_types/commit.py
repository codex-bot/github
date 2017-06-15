from data_types.user import User


class Commit:
    """
    Commit object

    https://developer.github.com/v3/repos/commits/

    Attributes:
        url: Commit URL in repo
        author: Commit author
        committer: Commit sender
        message: Commit messagee
        tree: Example {
          "url": "https://api.github.com/repos/octocat/Hello-World/tree/6dcb09b5b57875f334f61aebed695e2e4193db5e",
          "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e"
        },
        comment_count: Number of comments
        added: List of added files
        removed: List of removed files
        modified: List of modified files
    """

    def __init__(self, data):

        self.url = data.get('url', '')

        self.author = None
        if 'author' in data:
            self.author = User(data['author'])

        self.committer = None
        if 'committer' in data:
            self.committer = User(data['committer'])

        self.message = data.get('message', '')
        self.tree = data.get('tree', None)
        self.comment_count = data.get('comment_count', 0)

        self.added = data.get('added', [])
        self.removed = data.get('removed', [])
        self.modified = data.get('modified', [])


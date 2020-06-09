from data_types.branch import Branch
from data_types.repository import Repository
from data_types.user import User


class PullRequest:
    """
    GitHub Pull Request

    https://developer.github.com/v3/pulls/

    Attributes:
        id:             pull request id
        html_url:       pull request URL
        diff_url:       pull request URL .diff file
        issue_url:      issue object (JSON) source
        number:         PR's number in repository
        state:          open|closed

        title:          pull request title
        body:           pull request message

        user:           pull request author
        sender:         pull request sender

        merged:         whether this request closed or merged

        created_at:     Opening time
        closed_at:      Closing time. Null by default
        updated_at:     Updating time

        head:           head branch
        base:           base branch
        repository:     pull request repository

        commits_url:    list of commits
        review_comments_url:    review discussion
        requested_reviewers:    list of users that has been marked as reviewers
    """

    def __init__(self, data):

        # Internal GitHub id
        self.id = data.get('id', 0)

        # Title and Body
        self.title = data.get('title', '')
        self.body = data.get('body', '')

        # Public links
        self.html_url = data.get('html_url', '')
        self.diff_url = data.get('diff_url', '')
        self.issue_url = data.get('issue_url', '')
        self.commits_url = data.get('commits_url', '')
        self.review_comments_url = data.get('review_comments_url', '')

        # open | closed
        self.state = data.get('state', '')

        # Number in repository
        self.number = data.get('number', '')

        # Who opened
        self.user = None
        if 'user' in data:
            self.user = User(data['user'])

        # Who merged and sends
        self.sender = None
        if 'sender' in data:
            self.sender = User(data['sender'])

        # Whether this request closed or merged
        self.merged = data.get("merged", False)

        # Head branch
        self.head = None
        if 'head' in data:
            self.head = Branch(data['head'])

        # Base branch
        self.base = None
        if 'base' in data:
            self.base = Branch(data['base'])

        # Repository
        self.repository = None
        if 'repository' in data:
            self.repository = Repository(data['repository'])

        # Dates
        self.created_at = data.get('created_at', '')
        self.closed_at = data.get('closed_at', '')
        self.updated_at = data.get('updated_at', '')

        # Requested reviewers
        self.requested_reviewers = []
        if 'requested_reviewers' in data:
            for reviewer in data['requested_reviewers']:
                self.requested_reviewers.append(User(reviewer))

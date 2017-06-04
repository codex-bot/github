from github.data_types.user import User


class Repository:
    """
    GitHub Repository

    https://developer.github.com/v3/repos/

    Attributes:
        id: GitHub internal id
        name: Repository short name like "codex"
        full_name: Repository short full_name like "codex-team/codex"
        description: Optional description
        owner: Repository owner User
        private : true|false
        html_url: Public URL on github.com
        git_url: "git://github.com/baxterthehacker/public-repo.git"
        clone_url: "https://github.com/baxterthehacker/public-repo.git"
    """

    def __init__(self, data):

        # Internal GitHub id
        self.id = data.get('id', 0)

        self.name = data.get('name', '')
        self.full_name = data.get('full_name', '')
        self.description = data.get('description', '')

        # Public link
        self.html_url = data.get('html_url', '')

        # Owner represented as User
        self.owner = User(data['owner'])

        # Who closed
        self.closed_by = None
        if 'closed_by' in data:
            self.closed_by = User(data['closed_by'])

        self.private = data.get('private', 'false')
        self.git_url = data.get('git_url', '')
        self.clone_url = data.get('clone_url', '')

from data_types.user import User


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
        stargazers_count: 4756 — number of stars 
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

        self.private = data.get('private', 'false')
        self.git_url = data.get('git_url', '')
        self.clone_url = data.get('clone_url', '')
        
        self.stargazers_count = data.get('stargazers_count', 0)

class Organization:
    """
    GitHub Organization

    https://developer.github.com/v3/orgs/

    Attributes:
        id: GitHub internal id
        login: Organization name like "codex-team"
        description: Optional description
        url: API URL on github.com
    """

    def __init__(self, data):
        # Internal GitHub id
        self.id = data.get('id', 0)

        self.login = data.get('login', '')
        self.description = data.get('description', '')
        self.url = data.get('url', '')

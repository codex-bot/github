class User:
    """
    GitHub User

    https://developer.github.com/v3/users/

    Attributes:
        login: GitHub user name
        id: Internal GitHub id
        avatar_url: URL of image like "https://avatars.githubusercontent.com/u/6752317?v=3",
        html_url: Public user URL looks like "https://github.com/baxterthehacker",
    """

    def __init__(self, data):

        # Internal GitHub id
        self.id = data.get('id', 0)

        self.login = data.get('login', '')
        self.avatar_url = data.get('avatar_url', '')

        # Public link
        self.html_url = data.get('html_url', '')


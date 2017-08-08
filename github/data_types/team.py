class Team:
    """
    GitHub Team

    https://developer.github.com/v3/orgs/teams/

    Attributes:
        id: GitHub internal id
        url: "https://api.github.com/teams/1"
        name: The name of the team
        slug: Team name uri
        description: The description of the team.
        privacy: The level of privacy this team should have. Can be one of:
                 * secret - only visible to organization owners
                    and members of this team.
                 * closed - visible to all members of this organization.
                 Default: secret
        permission: Deprecated. The permission that new repositories will
                    be added to the team with when none is specified.
                    Can be one of:
                    * pull - team members can pull, but not push
                        to or administer newly-added repositories.
                    * push - team members can pull and push, but
                        not administer newly-added repositories.
                    * admin - team members can pull, push and
                        administer newly-added repositories.
                    Default: pull
        members_url: "https://api.github.com/teams/1/members{/member}"
        repositories_url: "https://api.github.com/teams/1/repos"
    """

    def __init__(self, data):

        self.id = data.get('id', 0)

        self.url = data.get('url', '')
        self.name = data.get('name', '')
        self.slug = data.get('slug', '')
        self.description = data.get('description', '')

        self.private = data.get('private', '')
        self.permission = data.get('permission', '')

        self.members_url = data.get('members_url', '')
        self.repositories_url = data.get('repositories_url', '')

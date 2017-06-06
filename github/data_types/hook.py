class Hook:
    """
    GitHub Webhook

    https://developer.github.com/v3/repos/hooks/#get-single-hook

    Attributes:
        type: webhook type, for example "Repository"
        id: Internal GitHub webhook id
        name: Use "web" for a webhook or use the name of a valid service.
              See https://api.github.com/hooks for the list of valid service names.
        active: true|false
        events: List of available events triggered by hook
        config: Example {
                    "content_type": "json",
                    "insecure_ssl": "0",
                    "url": "https://8344b572.ngrok.io/github/LC8RUXM8"
                },
        updated_at: "2017-06-06T20:47:58Z",
        created_at: "2017-06-06T20:47:58Z",
        url: "https://api.github.com/repos/codex-bot/playground/hooks/14209902",
        test_url: "https://api.github.com/repos/codex-bot/playground/hooks/14209902/test",
        ping_url: "https://api.github.com/repos/codex-bot/playground/hooks/14209902/pings",
        last_response: Example {
                        "code": null,
                        "status": "unused",
                        "message": null
                    }
    """

    def __init__(self, data):

        # Internal GitHub id
        self.id = data.get('id', 0)

        self.type = data.get('type', 0)
        self.name = data.get('name', 'web')
        self.active = data.get('active', 'false')

        # Configuration
        self.config = data.get('config', 'false')

        self.updated_at = data.get('updated_at', '')
        self.created_at = data.get('created_at', '')
        self.url = data.get('url', '')
        self.test_url = data.get('test_url', '')
        self.ping_url = data.get('ping_url', '')

        # Events list
        self.events = data.get('events', '')

        # Last response data
        self.last_response = data.get('last_response', '')


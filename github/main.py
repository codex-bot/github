import logging
from sdk.codexbot_sdk import CodexBot
from config import APPLICATION_TOKEN, APPLICATION_NAME, DB, URL, SERVER
from commands.help import CommandHelp
from commands.start import CommandStart
from events.ping import EventPing
from events.push import EventPush


class Github:

    def __init__(self):

        self.sdk = CodexBot(APPLICATION_NAME, SERVER['host'], SERVER['port'], db_config=DB, token=APPLICATION_TOKEN)

        self.sdk.log("Github module initialized")

        self.sdk.register_commands([
            ('github_help', 'help', CommandHelp(self.sdk).help),
            ('github_start', 'start', CommandStart(self.sdk).start)
        ])

        self.sdk.set_routes([
            ('POST', '/github/{user_token}', self.github_callback_handler)
        ])

        self.sdk.start_server()

    @CodexBot.http_response
    async def github_callback_handler(self, request):

        event_name = request['headers']['X-Github-Event']

        events = {
            'ping': EventPing(self.sdk),
            'push': EventPush(self.sdk),
        }

        if event_name not in events:
            self.sdk.log("Github webhook callback: unsupported event taken: {}".format(event_name))
            return {
                'status': 404
            }

        events[event_name].process(request['text'])

        return {
            'text': 'OK',
            'status': 200
        }

if __name__ == "__main__":
    github = Github()

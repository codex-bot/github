import logging
from sdk.codexbot_sdk import CodexBot
from config import APPLICATION_TOKEN, APPLICATION_NAME, DB, URL, SERVER
from commands.help import CommandHelp
from commands.start import CommandStart
from events.ping import EventPing


class Github:

    def __init__(self):

        self.sdk = CodexBot(APPLICATION_NAME, SERVER['host'], SERVER['port'], db_config=DB, token=APPLICATION_TOKEN)

        self.sdk.log("Github module initialized")

        self.sdk.register_commands([
            ('github_help', 'help', CommandHelp(sdk=self.sdk).help),
            ('github_start', 'start', CommandStart(sdk=self.sdk).start)
        ])

        self.sdk.set_routes([
            ('POST', '/github/{user_token}', self.github_callback_handler)
        ])

        self.sdk.start_server()

    @CodexBot.http_response
    async def github_callback_handler(self, result):
        events = {
            'ping': EventPing(sdk=self.sdk, headers=result['headers']).process
        }

        event = 'ping'
        events[event]()

        return {'text': '', 'status': 200}

if __name__ == "__main__":
    github = Github()

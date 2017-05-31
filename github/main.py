import random
import string
from time import time

from sdk.codexbot_sdk import CodexBot
from config import APPLICATION_TOKEN, APPLICATION_NAME, DB, URL, SERVER


class Github:

    def __init__(self):

        self.sdk = CodexBot(APPLICATION_NAME, SERVER['host'], SERVER['port'], db_config=DB, token=APPLICATION_TOKEN)

        self.sdk.log("Github module initialized")

        self.sdk.register_commands([
            ('github_help', 'help', self.help),
            # ('github_start', 'start', self.start)
        ])

        self.sdk.set_routes([
            # ('POST', '/github/{user_token}', self.github_route_handler)
        ])

        self.sdk.start_server()

    #
    #
    # HELP
    # todo: move to the class
    #

    async def help(self, payload):
        self.sdk.log("/help handler fired with payload {}".format(payload))
        await self.sdk.send_to_chat(
            payload["chat"],
            "I can`t help you."
        )

if __name__ == "__main__":
    github = Github()

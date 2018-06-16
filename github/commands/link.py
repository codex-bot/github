from classes.chat_controller import ChatController
from config import URL
from .base import CommandBase


class CommandLink(CommandBase):

    async def __call__(self, payload):
        self.sdk.log("/github_link handler fired with payload {}".format(payload))

        self.set_bot(payload)

        user_token = ChatController(self.sdk).register_chat(payload['chat'], self.bot)

        link = "{}/github/{}".format(URL, user_token)

        await self.send(
            payload["chat"],
            "Link to the chat: {}".format(link)
        )

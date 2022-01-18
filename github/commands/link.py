from classes.chat_controller import ChatController
from settings import URL
from .base import CommandBase


class CommandLink(CommandBase):

    async def __call__(self, payload):
        self.sdk.log("/github_link handler fired with payload {}".format(payload))

        self.set_bot(payload)

        chat = ChatController(self.sdk).get_chat(payload['chat'], self.bot)

        link = "{}/github/{}".format(URL, chat["user"])

        await self.send(
            payload["chat"],
            "Link to the chat: {}".format(link)
        )
